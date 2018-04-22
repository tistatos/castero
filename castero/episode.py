import os
import threading
from castero import helpers
from castero.datafile import DataFile


class Episode:
    """The Episode class.

    This class represents a single episode from a podcast feed.
    """
    def __init__(self, feed, title=None, description=None, link=None,
                 pubdate=None, copyright=None, enclosure=None) -> None:
        """Initializes the object.

        At least one of a title or description must be specified.

        Args:
            feed: the feed that this episode is a part of
            title: (optional) the title of the episode
            description: (optional) the description of the episode
            link: (optional) a link to the episode
            pubdate: (optional) the date the episode was published, as a string
            copyright: (optional) the copyright notice of the episode
            enclosure: (optional) a url to a media file
        """
        assert title is not None or description is not None

        self._feed = feed
        self._title = title
        self._description = description
        self._link = link
        self._pubdate = pubdate
        self._copyright = copyright
        self._enclosure = enclosure

    def __str__(self) -> str:
        """Represent this object as a single-line string.

        Returns:
            string: this episode's title, if it exists, else its description
        """
        if self._title is not None:
            representation = self._title
        else:
            representation = self._description
        return representation.split('\n')[0]

    def get_playable(self) -> str:
        """Gets a playable path for this episode.

        This method checks whether the episode is available on the disk, giving
        the path to that file if so. Otherwise, simply return the episode's
        enclosure, which is probably a URL.

        Returns:
            str: a path to a playable file for this episode
        """
        playable = self.enclosure

        feed_dirname = helpers.sanitize_path(str(self._feed))
        episode_partial_filename = helpers.sanitize_path(str(self))
        feed_directory = os.path.join(DataFile.DOWNLOADED_DIR, feed_dirname)

        if os.path.exists(feed_directory):
            for File in os.listdir(feed_directory):
                if File.startswith(episode_partial_filename + '.'):
                    playable = os.path.join(feed_directory, File)

        return playable

    def download(self, display=None):
        """Downloads this episode to the file system.

        This method currently only supports downloading from an external URL.
        In the future, it may be worthwhile to determine whether the episode's
        source is a local file and simply copy it instead.

        Args:
            display: (optional) the display to write status updates to
        """
        if self._enclosure is None:
            if display is not None:
                display.update_status("Download failed: episode does not have"
                                      " a valid media source")
            return

        feed_dirname = helpers.sanitize_path(str(self._feed))
        feed_directory = os.path.join(DataFile.DOWNLOADED_DIR,
                                      feed_dirname)
        episode_partial_filename = helpers.sanitize_path(str(self))
        extension = os.path.splitext(self._enclosure)[1].split('?')[0]
        output_path = os.path.join(feed_directory,
                                   episode_partial_filename + str(extension))
        DataFile.ensure_path(output_path)

        if display is not None:
            display.update_status("Starting episode download...")

        t = threading.Thread(
            target=DataFile.download_to_file,
            args=[self._enclosure, output_path, display]
        )
        t.start()

    @property
    def title(self) -> str:
        result = self._title
        if result is None:
            result = "Title not available."
        return result

    @property
    def description(self) -> str:
        result = self._description
        if result is None:
            result = "Description not available."
        return result

    @property
    def link(self) -> str:
        result = self._link
        if result is None:
            result = "Link not available."
        return result

    @property
    def pubdate(self) -> str:
        result = self._pubdate
        if result is None:
            result = "Publish date not available."
        return result

    @property
    def copyright(self) -> str:
        result = self._copyright
        if result is None:
            result = "Copyright not available."
        return result

    @property
    def enclosure(self) -> str:
        result = self._enclosure
        if result is None:
            result = "Enclosure not available."
        return result

    @property
    def downloaded(self) -> str:
        found_downloaded = False
        feed_dirname = helpers.sanitize_path(str(self._feed))
        episode_partial_filename = helpers.sanitize_path(str(self))
        feed_directory = os.path.join(DataFile.DOWNLOADED_DIR, feed_dirname)

        if os.path.exists(feed_directory):
            for File in os.listdir(feed_directory):
                if File.startswith(episode_partial_filename + '.'):
                    found_downloaded = True

        if found_downloaded:
            result = "Episode downloaded and available for offline playback."
        else:
            result = "Episode not downloaded."
        return result
