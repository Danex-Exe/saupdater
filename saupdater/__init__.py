from ._imports import *
from .logger import Logger
from .errors import *

__version__ = "1.0.0-alpha"
__all__ = ['Updater']

class Updater:
    LINK_FORMAT = "https://github.com/username/repository"
    logger = Logger(title="SAUPDATER", log_file="saupdater.log")

    def __init__(self, link: str, branch: str = 'main', show_logs: bool = True) -> None:
        self._link = link
        self.path = self._get_path()
        self.branch = branch
        self._show_logs = show_logs

        if not re.match(r'^[a-zA-Z0-9_\-\.]+$', branch):
            raise ValueError(f"Invalid branch name: {branch}")

        result, username, repository = self._check_link()
        if result:
            self.username = username
            self.repository = repository.replace('.git', '')
        else:
            raise LinkError(self._link, self.LINK_FORMAT)

        self._get_local_version()

    def _get_local_version(self) -> None:
        self.version_file_path = self.path + '\\.version'

        if not os.path.exists(self.version_file_path):
            raise GetLocalVersionError(self.version_file_path)

        try:
            self.local_version = open(self.version_file_path).readline().strip()
            pattern = r'(?:\d+.)+'
            if not re.search(pattern, self.local_version):
                raise LocalVersionError(self.version_file_path, self.local_version)
        except:
            raise GetLocalVersionError(self.version_file_path)

    def _check_link(self) -> tuple:
        pattern = r'(https?)://github\.com/(?P<username>[a-zA-Z0-9_-]+)(/(?P<repository>[^/]+))?(\.git)?/?'
        match = re.search(pattern, self._link)

        if match \
            and (username := match.group('username')) \
            and (repository := match.group('repository')):

            return (True, username, repository)
        return (False, '', '')

    def _get_path(self) -> str:
        return '\\'.join(sys.argv[0].rsplit('\\')[:-1:])

    def _get_remote_origin(self) -> None:
        self._remote_origin = self._check_remote_origin()
        if not self._remote_origin \
            or self._remote_origin == '':
            raise RemoteOriginNotFoundError()

    def _check_remote_origin(self) -> str:
        try:
            result = subprocess.run(
                ['git', 'remote', 'get-url', 'origin'],
                cwd=self.path,
                capture_output=True,
                text=True,
                check=True
            )
            return result.stdout.strip()
        except (subprocess.CalledProcessError, FileNotFoundError):
            return ""

    def check(self) -> None:
        self._get_local_version()
        self._get_remote_origin()

        url = f"https://raw.githubusercontent.com/{self.username}/{self.repository}/refs/heads/{self.branch}/.version"
        try:
            response = requests.get(url)
            response.raise_for_status()
            remote_version = response.text.strip()

            if remote_version == self.local_version:
                return self.log(f'You have latest version {self.local_version}')

            try:
                result = subprocess.run(
                    ['git', 'pull'],
                    cwd=self.path,
                    capture_output=True,
                    text=True,
                    check=True
                )
                result = result.stdout.strip().split('\n')

                if 'Already up to date.' in result[0]:
                    with open(self.version_file_path, 'w') as version_file:
                        version_file.write(remote_version)

                    return self.log(f'You have latest version {self.local_version}')

                self.logger.warning(f'New update available {remote_version}')
                self.log(result[0])
                return self.log('The update is successful')

            except Exception as e:
                raise GitPullError(str(e))

        except:
            raise GetGitHubVersionError(url)

    def log(self, message: str) -> None:
        if self._show_logs:
            self.logger.info(message)