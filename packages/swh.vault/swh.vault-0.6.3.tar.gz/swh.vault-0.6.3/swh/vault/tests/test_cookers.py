# Copyright (C) 2017-2020  The Software Heritage developers
# See the AUTHORS file at the top-level directory of this distribution
# License: GNU General Public License version 3, or any later version
# See top-level LICENSE file for more information

import contextlib
import datetime
import glob
import gzip
import io
import os
import pathlib
import shutil
import subprocess
import tarfile
import tempfile
import unittest
import unittest.mock

import dulwich.fastexport
import dulwich.index
import dulwich.objects
import dulwich.porcelain
import dulwich.repo
import pytest

from swh.loader.git.from_disk import GitLoaderFromDisk
from swh.model import from_disk, hashutil
from swh.model.model import (
    Directory,
    DirectoryEntry,
    Person,
    Revision,
    RevisionType,
    TimestampWithTimezone,
)
from swh.vault.cookers import DirectoryCooker, GitBareCooker, RevisionGitfastCooker
from swh.vault.tests.vault_testing import hash_content
from swh.vault.to_disk import HIDDEN_MESSAGE, SKIPPED_MESSAGE


class TestRepo:
    """A tiny context manager for a test git repository, with some utility
    functions to perform basic git stuff.
    """

    def __init__(self, repo_dir=None):
        self.repo_dir = repo_dir

    def __enter__(self):
        if self.repo_dir:
            self.tmp_dir = None
            self.repo = dulwich.repo.Repo(self.repo_dir)
        else:
            self.tmp_dir = tempfile.TemporaryDirectory(prefix="tmp-vault-repo-")
            self.repo_dir = self.tmp_dir.__enter__()
            self.repo = dulwich.repo.Repo.init(self.repo_dir)
        self.author_name = b"Test Author"
        self.author_email = b"test@softwareheritage.org"
        self.author = b"%s <%s>" % (self.author_name, self.author_email)
        self.base_date = 258244200
        self.counter = 0
        return pathlib.Path(self.repo_dir)

    def __exit__(self, exc, value, tb):
        if self.tmp_dir is not None:
            self.tmp_dir.__exit__(exc, value, tb)
            self.repo_dir = None

    def checkout(self, rev_sha):
        rev = self.repo[rev_sha]
        dulwich.index.build_index_from_tree(
            self.repo_dir, self.repo.index_path(), self.repo.object_store, rev.tree
        )

    def git_shell(self, *cmd, stdout=subprocess.DEVNULL, **kwargs):
        name = self.author_name
        email = self.author_email
        date = "%d +0000" % (self.base_date + self.counter)
        env = {
            # Set git commit format
            "GIT_AUTHOR_NAME": name,
            "GIT_AUTHOR_EMAIL": email,
            "GIT_AUTHOR_DATE": date,
            "GIT_COMMITTER_NAME": name,
            "GIT_COMMITTER_EMAIL": email,
            "GIT_COMMITTER_DATE": date,
            # Ignore all the system-wide and user configurations
            "GIT_CONFIG_NOSYSTEM": "1",
            "HOME": str(self.tmp_dir),
            "XDG_CONFIG_HOME": str(self.tmp_dir),
        }
        kwargs.setdefault("env", {}).update(env)

        subprocess.check_call(
            ("git", "-C", self.repo_dir) + cmd, stdout=stdout, **kwargs
        )

    def commit(self, message="Commit test\n", ref=b"HEAD"):
        """Commit the current working tree in a new commit with message on
        the branch 'ref'.

        At the end of the commit, the reference should stay the same
        and the index should be clean.

        """
        paths = [
            os.path.relpath(path, self.repo_dir)
            for path in glob.glob(self.repo_dir + "/**/*", recursive=True)
        ]
        self.repo.stage(paths)
        message = message.encode() + b"\n"
        ret = self.repo.do_commit(
            message=message,
            committer=self.author,
            commit_timestamp=self.base_date + self.counter,
            commit_timezone=0,
            ref=ref,
        )
        self.counter += 1

        # committing on another branch leaves
        # dangling files in index
        if ref != b"HEAD":
            # XXX this should work (but does not)
            # dulwich.porcelain.reset(self.repo, 'hard')
            self.git_shell("reset", "--hard", "HEAD")
        return ret

    def merge(self, parent_sha_list, message="Merge branches."):
        self.git_shell(
            "merge",
            "--allow-unrelated-histories",
            "-m",
            message,
            *[p.decode() for p in parent_sha_list],
        )
        self.counter += 1
        return self.repo.refs[b"HEAD"]

    def print_debug_graph(self, reflog=False):
        args = ["log", "--all", "--graph", "--decorate"]
        if reflog:
            args.append("--reflog")
        self.git_shell(*args, stdout=None)


@pytest.fixture
def git_loader(swh_storage,):
    """Instantiate a Git Loader using the storage instance as storage.

    """

    def _create_loader(directory):
        return GitLoaderFromDisk(
            swh_storage,
            "fake_origin",
            directory=directory,
            visit_date=datetime.datetime.now(datetime.timezone.utc),
        )

    return _create_loader


@contextlib.contextmanager
def cook_extract_directory_dircooker(storage, obj_id, fsck=True):
    """Context manager that cooks a directory and extract it."""
    backend = unittest.mock.MagicMock()
    backend.storage = storage
    cooker = DirectoryCooker("directory", obj_id, backend=backend, storage=storage)
    cooker.fileobj = io.BytesIO()
    assert cooker.check_exists()
    cooker.prepare_bundle()
    cooker.fileobj.seek(0)
    with tempfile.TemporaryDirectory(prefix="tmp-vault-extract-") as td:
        with tarfile.open(fileobj=cooker.fileobj, mode="r") as tar:
            tar.extractall(td)
        yield pathlib.Path(td) / hashutil.hash_to_hex(obj_id)
    cooker.storage = None


@contextlib.contextmanager
def cook_extract_directory_gitfast(storage, obj_id, fsck=True):
    """Context manager that cooks a revision containing a directory and extract it,
    using RevisionGitfastCooker"""
    test_repo = TestRepo()
    with test_repo as p:
        date = TimestampWithTimezone.from_datetime(
            datetime.datetime.now(datetime.timezone.utc)
        )
        revision = Revision(
            directory=obj_id,
            message=b"dummy message",
            author=Person.from_fullname(b"someone"),
            committer=Person.from_fullname(b"someone"),
            date=date,
            committer_date=date,
            type=RevisionType.GIT,
            synthetic=False,
        )
        storage.revision_add([revision])

    with cook_stream_revision_gitfast(storage, revision.id) as stream, test_repo as p:
        processor = dulwich.fastexport.GitImportProcessor(test_repo.repo)
        processor.import_stream(stream)
        test_repo.checkout(b"HEAD")
        shutil.rmtree(p / ".git")
        yield p


@contextlib.contextmanager
def cook_extract_directory_git_bare(
    storage, obj_id, fsck=True, direct_objstorage=False
):
    """Context manager that cooks a revision and extract it,
    using GitBareCooker"""
    backend = unittest.mock.MagicMock()
    backend.storage = storage

    # Cook the object
    cooker = GitBareCooker(
        "directory",
        obj_id,
        backend=backend,
        storage=storage,
        objstorage=storage.objstorage if direct_objstorage else None,
    )
    cooker.use_fsck = fsck  # Some tests try edge-cases that git-fsck rejects
    cooker.fileobj = io.BytesIO()
    assert cooker.check_exists()
    cooker.prepare_bundle()
    cooker.fileobj.seek(0)

    # Extract it
    with tempfile.TemporaryDirectory(prefix="tmp-vault-extract-") as td:
        with tarfile.open(fileobj=cooker.fileobj, mode="r") as tar:
            tar.extractall(td)

        # Clone it with Dulwich
        with tempfile.TemporaryDirectory(prefix="tmp-vault-clone-") as clone_dir:
            clone_dir = pathlib.Path(clone_dir)
            subprocess.check_call(
                [
                    "git",
                    "clone",
                    os.path.join(td, f"swh:1:dir:{obj_id.hex()}.git"),
                    clone_dir,
                ]
            )
            shutil.rmtree(clone_dir / ".git")
            yield clone_dir


@pytest.fixture(
    scope="module",
    params=[
        cook_extract_directory_dircooker,
        cook_extract_directory_gitfast,
        cook_extract_directory_git_bare,
    ],
)
def cook_extract_directory(request):
    """A fixture that is instantiated as either cook_extract_directory_dircooker or
    cook_extract_directory_git_bare."""
    return request.param


@contextlib.contextmanager
def cook_stream_revision_gitfast(storage, obj_id):
    """Context manager that cooks a revision and stream its fastexport."""
    backend = unittest.mock.MagicMock()
    backend.storage = storage
    cooker = RevisionGitfastCooker(
        "revision_gitfast", obj_id, backend=backend, storage=storage
    )
    cooker.fileobj = io.BytesIO()
    assert cooker.check_exists()
    cooker.prepare_bundle()
    cooker.fileobj.seek(0)
    fastexport_stream = gzip.GzipFile(fileobj=cooker.fileobj)
    yield fastexport_stream
    cooker.storage = None


@contextlib.contextmanager
def cook_extract_revision_gitfast(storage, obj_id, fsck=True):
    """Context manager that cooks a revision and extract it,
    using RevisionGitfastCooker"""
    test_repo = TestRepo()
    with cook_stream_revision_gitfast(storage, obj_id) as stream, test_repo as p:
        processor = dulwich.fastexport.GitImportProcessor(test_repo.repo)
        processor.import_stream(stream)
        yield test_repo, p


@contextlib.contextmanager
def cook_extract_revision_git_bare(storage, obj_id, fsck=True):
    """Context manager that cooks a revision and extract it,
    using GitBareCooker"""
    backend = unittest.mock.MagicMock()
    backend.storage = storage

    # Cook the object
    cooker = GitBareCooker("revision", obj_id, backend=backend, storage=storage)
    cooker.use_fsck = fsck  # Some tests try edge-cases that git-fsck rejects
    cooker.fileobj = io.BytesIO()
    assert cooker.check_exists()
    cooker.prepare_bundle()
    cooker.fileobj.seek(0)

    # Extract it
    with tempfile.TemporaryDirectory(prefix="tmp-vault-extract-") as td:
        with tarfile.open(fileobj=cooker.fileobj, mode="r") as tar:
            tar.extractall(td)

        # Clone it with Dulwich
        with tempfile.TemporaryDirectory(prefix="tmp-vault-clone-") as clone_dir:
            clone_dir = pathlib.Path(clone_dir)
            subprocess.check_call(
                [
                    "git",
                    "clone",
                    os.path.join(td, f"swh:1:rev:{obj_id.hex()}.git"),
                    clone_dir,
                ]
            )
            test_repo = TestRepo(clone_dir)
            with test_repo:
                yield test_repo, clone_dir


@pytest.fixture(
    scope="module",
    params=[cook_extract_revision_gitfast, cook_extract_revision_git_bare],
)
def cook_extract_revision(request):
    """A fixture that is instantiated as either cook_extract_revision_gitfast or
    cook_extract_revision_git_bare."""
    return request.param


TEST_CONTENT = (
    "   test content\n" "and unicode \N{BLACK HEART SUIT}\n" " and trailing spaces   "
)
TEST_EXECUTABLE = b"\x42\x40\x00\x00\x05"


class TestDirectoryCooker:
    def test_directory_simple(self, git_loader, cook_extract_directory):
        repo = TestRepo()
        with repo as rp:
            (rp / "file").write_text(TEST_CONTENT)
            (rp / "executable").write_bytes(TEST_EXECUTABLE)
            (rp / "executable").chmod(0o755)
            (rp / "link").symlink_to("file")
            (rp / "dir1/dir2").mkdir(parents=True)
            (rp / "dir1/dir2/file").write_text(TEST_CONTENT)
            c = repo.commit()
            loader = git_loader(str(rp))
            loader.load()

            obj_id_hex = repo.repo[c].tree.decode()
            obj_id = hashutil.hash_to_bytes(obj_id_hex)

        with cook_extract_directory(loader.storage, obj_id) as p:
            assert (p / "file").stat().st_mode == 0o100644
            assert (p / "file").read_text() == TEST_CONTENT
            assert (p / "executable").stat().st_mode == 0o100755
            assert (p / "executable").read_bytes() == TEST_EXECUTABLE
            assert (p / "link").is_symlink()
            assert os.readlink(str(p / "link")) == "file"
            assert (p / "dir1/dir2/file").stat().st_mode == 0o100644
            assert (p / "dir1/dir2/file").read_text() == TEST_CONTENT

            directory = from_disk.Directory.from_disk(path=bytes(p))
            assert obj_id_hex == hashutil.hash_to_hex(directory.hash)

    def test_directory_filtered_objects(self, git_loader, cook_extract_directory):
        repo = TestRepo()
        with repo as rp:
            file_1, id_1 = hash_content(b"test1")
            file_2, id_2 = hash_content(b"test2")
            file_3, id_3 = hash_content(b"test3")

            (rp / "file").write_bytes(file_1)
            (rp / "hidden_file").write_bytes(file_2)
            (rp / "absent_file").write_bytes(file_3)

            c = repo.commit()
            loader = git_loader(str(rp))
            loader.load()

            obj_id_hex = repo.repo[c].tree.decode()
            obj_id = hashutil.hash_to_bytes(obj_id_hex)

        # FIXME: storage.content_update() should be changed to allow things
        # like that
        with loader.storage.get_db().transaction() as cur:
            cur.execute(
                """update content set status = 'visible'
                           where sha1 = %s""",
                (id_1,),
            )
            cur.execute(
                """update content set status = 'hidden'
                           where sha1 = %s""",
                (id_2,),
            )

            cur.execute(
                """
                insert into skipped_content
                    (sha1, sha1_git, sha256, blake2s256, length, reason)
                select sha1, sha1_git, sha256, blake2s256, length, 'no reason'
                from content
                where sha1 = %s
                """,
                (id_3,),
            )

            cur.execute("delete from content where sha1 = %s", (id_3,))

        with cook_extract_directory(loader.storage, obj_id) as p:
            assert (p / "file").read_bytes() == b"test1"
            assert (p / "hidden_file").read_bytes() == HIDDEN_MESSAGE
            assert (p / "absent_file").read_bytes() == SKIPPED_MESSAGE

    def test_directory_bogus_perms(self, git_loader, cook_extract_directory):
        # Some early git repositories have 664/775 permissions... let's check
        # if all the weird modes are properly normalized in the directory
        # cooker.
        repo = TestRepo()
        with repo as rp:
            (rp / "file").write_text(TEST_CONTENT)
            (rp / "file").chmod(0o664)
            (rp / "executable").write_bytes(TEST_EXECUTABLE)
            (rp / "executable").chmod(0o775)
            (rp / "wat").write_text(TEST_CONTENT)
            (rp / "wat").chmod(0o604)

            # Disable mode cleanup
            with unittest.mock.patch("dulwich.index.cleanup_mode", lambda mode: mode):
                c = repo.commit()

            # Make sure Dulwich didn't normalize the permissions itself.
            # (if it did, then the test can't check the cooker normalized them)
            tree_id = repo.repo[c].tree
            assert {entry.mode for entry in repo.repo[tree_id].items()} == {
                0o100775,
                0o100664,
                0o100604,
            }

            # Disable mode checks
            with unittest.mock.patch("dulwich.objects.Tree.check", lambda self: None):
                loader = git_loader(str(rp))
                loader.load()

            # Make sure swh-loader didn't normalize them either
            dir_entries = loader.storage.directory_ls(hashutil.bytehex_to_hash(tree_id))
            assert {entry["perms"] for entry in dir_entries} == {
                0o100664,
                0o100775,
                0o100604,
            }

            obj_id_hex = repo.repo[c].tree.decode()
            obj_id = hashutil.hash_to_bytes(obj_id_hex)

        with cook_extract_directory(loader.storage, obj_id) as p:
            assert (p / "file").stat().st_mode == 0o100644
            assert (p / "executable").stat().st_mode == 0o100755
            assert (p / "wat").stat().st_mode == 0o100644

    @pytest.mark.parametrize("direct_objstorage", [True, False])
    def test_directory_objstorage(
        self, swh_storage, git_loader, mocker, direct_objstorage
    ):
        """Like test_directory_simple, but using swh_objstorage directly, without
        going through swh_storage.content_get_data()"""
        repo = TestRepo()
        with repo as rp:
            (rp / "file").write_text(TEST_CONTENT)
            (rp / "executable").write_bytes(TEST_EXECUTABLE)
            (rp / "executable").chmod(0o755)
            (rp / "link").symlink_to("file")
            (rp / "dir1/dir2").mkdir(parents=True)
            (rp / "dir1/dir2/file").write_text(TEST_CONTENT)
            c = repo.commit()
            loader = git_loader(str(rp))
            loader.load()

            obj_id_hex = repo.repo[c].tree.decode()
            obj_id = hashutil.hash_to_bytes(obj_id_hex)

        # Set-up spies
        storage_content_get_data = mocker.patch.object(
            swh_storage, "content_get_data", wraps=swh_storage.content_get_data
        )
        objstorage_content_batch = mocker.patch.object(
            swh_storage.objstorage, "get_batch", wraps=swh_storage.objstorage.get_batch
        )

        with cook_extract_directory_git_bare(
            loader.storage, obj_id, direct_objstorage=direct_objstorage
        ) as p:
            assert (p / "file").stat().st_mode == 0o100644
            assert (p / "file").read_text() == TEST_CONTENT
            assert (p / "executable").stat().st_mode == 0o100755
            assert (p / "executable").read_bytes() == TEST_EXECUTABLE
            assert (p / "link").is_symlink()
            assert os.readlink(str(p / "link")) == "file"
            assert (p / "dir1/dir2/file").stat().st_mode == 0o100644
            assert (p / "dir1/dir2/file").read_text() == TEST_CONTENT

            directory = from_disk.Directory.from_disk(path=bytes(p))
            assert obj_id_hex == hashutil.hash_to_hex(directory.hash)

        if direct_objstorage:
            storage_content_get_data.assert_not_called()
            objstorage_content_batch.assert_called()
        else:
            storage_content_get_data.assert_called()
            objstorage_content_batch.assert_not_called()

    def test_directory_revision_data(self, swh_storage):
        target_rev = "0e8a3ad980ec179856012b7eecf4327e99cd44cd"

        dir = Directory(
            entries=(
                DirectoryEntry(
                    name=b"submodule",
                    type="rev",
                    target=hashutil.hash_to_bytes(target_rev),
                    perms=0o100644,
                ),
            ),
        )
        swh_storage.directory_add([dir])

        with cook_extract_directory_dircooker(swh_storage, dir.id, fsck=False) as p:
            assert (p / "submodule").is_symlink()
            assert os.readlink(str(p / "submodule")) == target_rev


class TestRevisionCooker:
    def test_revision_simple(self, git_loader, cook_extract_revision):
        #
        #     1--2--3--4--5--6--7
        #
        repo = TestRepo()
        with repo as rp:
            (rp / "file1").write_text(TEST_CONTENT)
            repo.commit("add file1")
            (rp / "file2").write_text(TEST_CONTENT)
            repo.commit("add file2")
            (rp / "dir1/dir2").mkdir(parents=True)
            (rp / "dir1/dir2/file").write_text(TEST_CONTENT)
            repo.commit("add dir1/dir2/file")
            (rp / "bin1").write_bytes(TEST_EXECUTABLE)
            (rp / "bin1").chmod(0o755)
            repo.commit("add bin1")
            (rp / "link1").symlink_to("file1")
            repo.commit("link link1 to file1")
            (rp / "file2").unlink()
            repo.commit("remove file2")
            (rp / "bin1").rename(rp / "bin")
            repo.commit("rename bin1 to bin")
            loader = git_loader(str(rp))
            loader.load()
            obj_id_hex = repo.repo.refs[b"HEAD"].decode()
            obj_id = hashutil.hash_to_bytes(obj_id_hex)

        with cook_extract_revision(loader.storage, obj_id) as (ert, p):
            ert.checkout(b"HEAD")
            assert (p / "file1").stat().st_mode == 0o100644
            assert (p / "file1").read_text() == TEST_CONTENT
            assert (p / "link1").is_symlink()
            assert os.readlink(str(p / "link1")) == "file1"
            assert (p / "bin").stat().st_mode == 0o100755
            assert (p / "bin").read_bytes() == TEST_EXECUTABLE
            assert (p / "dir1/dir2/file").read_text() == TEST_CONTENT
            assert (p / "dir1/dir2/file").stat().st_mode == 0o100644
            assert ert.repo.refs[b"HEAD"].decode() == obj_id_hex

    def test_revision_two_roots(self, git_loader, cook_extract_revision):
        #
        #    1----3---4
        #        /
        #   2----
        #
        repo = TestRepo()
        with repo as rp:
            (rp / "file1").write_text(TEST_CONTENT)
            c1 = repo.commit("Add file1")
            del repo.repo.refs[b"refs/heads/master"]  # git update-ref -d HEAD
            (rp / "file2").write_text(TEST_CONTENT)
            repo.commit("Add file2")
            repo.merge([c1])
            (rp / "file3").write_text(TEST_CONTENT)
            repo.commit("add file3")
            obj_id_hex = repo.repo.refs[b"HEAD"].decode()
            obj_id = hashutil.hash_to_bytes(obj_id_hex)
            loader = git_loader(str(rp))
            loader.load()

        with cook_extract_revision(loader.storage, obj_id) as (ert, p):
            assert ert.repo.refs[b"HEAD"].decode() == obj_id_hex

    def test_revision_two_double_fork_merge(self, git_loader, cook_extract_revision):
        #
        #     2---4---6
        #    /   /   /
        #   1---3---5
        #
        repo = TestRepo()
        with repo as rp:
            (rp / "file1").write_text(TEST_CONTENT)
            c1 = repo.commit("Add file1")
            repo.repo.refs[b"refs/heads/c1"] = c1

            (rp / "file2").write_text(TEST_CONTENT)
            repo.commit("Add file2")

            (rp / "file3").write_text(TEST_CONTENT)
            c3 = repo.commit("Add file3", ref=b"refs/heads/c1")
            repo.repo.refs[b"refs/heads/c3"] = c3

            repo.merge([c3])

            (rp / "file5").write_text(TEST_CONTENT)
            c5 = repo.commit("Add file3", ref=b"refs/heads/c3")

            repo.merge([c5])

            obj_id_hex = repo.repo.refs[b"HEAD"].decode()
            obj_id = hashutil.hash_to_bytes(obj_id_hex)
            loader = git_loader(str(rp))
            loader.load()

        with cook_extract_revision(loader.storage, obj_id) as (ert, p):
            assert ert.repo.refs[b"HEAD"].decode() == obj_id_hex

    def test_revision_triple_merge(self, git_loader, cook_extract_revision):
        #
        #       .---.---5
        #      /   /   /
        #     2   3   4
        #    /   /   /
        #   1---.---.
        #
        repo = TestRepo()
        with repo as rp:
            (rp / "file1").write_text(TEST_CONTENT)
            c1 = repo.commit("Commit 1")
            repo.repo.refs[b"refs/heads/b1"] = c1
            repo.repo.refs[b"refs/heads/b2"] = c1

            repo.commit("Commit 2")
            c3 = repo.commit("Commit 3", ref=b"refs/heads/b1")
            c4 = repo.commit("Commit 4", ref=b"refs/heads/b2")
            repo.merge([c3, c4])

            obj_id_hex = repo.repo.refs[b"HEAD"].decode()
            obj_id = hashutil.hash_to_bytes(obj_id_hex)
            loader = git_loader(str(rp))
            loader.load()

        with cook_extract_revision(loader.storage, obj_id) as (ert, p):
            assert ert.repo.refs[b"HEAD"].decode() == obj_id_hex

    def test_revision_filtered_objects(self, git_loader, cook_extract_revision):
        repo = TestRepo()
        with repo as rp:
            file_1, id_1 = hash_content(b"test1")
            file_2, id_2 = hash_content(b"test2")
            file_3, id_3 = hash_content(b"test3")

            (rp / "file").write_bytes(file_1)
            (rp / "hidden_file").write_bytes(file_2)
            (rp / "absent_file").write_bytes(file_3)

            repo.commit()
            obj_id_hex = repo.repo.refs[b"HEAD"].decode()
            obj_id = hashutil.hash_to_bytes(obj_id_hex)
            loader = git_loader(str(rp))
            loader.load()

        # FIXME: storage.content_update() should be changed to allow things
        # like that
        with loader.storage.get_db().transaction() as cur:
            cur.execute(
                """update content set status = 'visible'
                           where sha1 = %s""",
                (id_1,),
            )
            cur.execute(
                """update content set status = 'hidden'
                           where sha1 = %s""",
                (id_2,),
            )

            cur.execute(
                """
                insert into skipped_content
                    (sha1, sha1_git, sha256, blake2s256, length, reason)
                select sha1, sha1_git, sha256, blake2s256, length, 'no reason'
                from content
                where sha1 = %s
                """,
                (id_3,),
            )

            cur.execute("delete from content where sha1 = %s", (id_3,))

        with cook_extract_revision(loader.storage, obj_id) as (ert, p):
            ert.checkout(b"HEAD")
            assert (p / "file").read_bytes() == b"test1"
            assert (p / "hidden_file").read_bytes() == HIDDEN_MESSAGE
            assert (p / "absent_file").read_bytes() == SKIPPED_MESSAGE

    def test_revision_null_fields(self, git_loader, cook_extract_revision):
        # Our schema doesn't enforce a lot of non-null revision fields. We need
        # to check these cases don't break the cooker.
        repo = TestRepo()
        with repo as rp:
            (rp / "file").write_text(TEST_CONTENT)
            c = repo.commit("initial commit")
            loader = git_loader(str(rp))
            loader.load()
            repo.repo.refs[b"HEAD"].decode()
            dir_id_hex = repo.repo[c].tree.decode()
            dir_id = hashutil.hash_to_bytes(dir_id_hex)

        test_revision = Revision(
            message=b"",
            author=Person(name=None, email=None, fullname=b""),
            date=None,
            committer=Person(name=None, email=None, fullname=b""),
            committer_date=None,
            parents=(),
            type=RevisionType.GIT,
            directory=dir_id,
            metadata={},
            synthetic=True,
        )

        storage = loader.storage
        storage.revision_add([test_revision])

        with cook_extract_revision(storage, test_revision.id, fsck=False) as (ert, p):
            ert.checkout(b"HEAD")
            assert (p / "file").stat().st_mode == 0o100644

    def test_revision_revision_data(self, swh_storage):
        target_rev = "0e8a3ad980ec179856012b7eecf4327e99cd44cd"

        dir = Directory(
            entries=(
                DirectoryEntry(
                    name=b"submodule",
                    type="rev",
                    target=hashutil.hash_to_bytes(target_rev),
                    perms=0o100644,
                ),
            ),
        )
        swh_storage.directory_add([dir])

        rev = Revision(
            message=b"",
            author=Person(name=None, email=None, fullname=b""),
            date=None,
            committer=Person(name=None, email=None, fullname=b""),
            committer_date=None,
            parents=(),
            type=RevisionType.GIT,
            directory=dir.id,
            metadata={},
            synthetic=True,
        )
        swh_storage.revision_add([rev])

        with cook_stream_revision_gitfast(swh_storage, rev.id) as stream:
            pattern = "M 160000 {} submodule".format(target_rev).encode()
            assert pattern in stream.read()
