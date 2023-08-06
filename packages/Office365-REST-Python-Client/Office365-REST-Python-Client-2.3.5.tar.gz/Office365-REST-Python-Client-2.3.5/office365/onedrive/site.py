from office365.base_item import BaseItem
from office365.onedrive.columnDefinitionCollection import ColumnDefinitionCollection
from office365.onedrive.contentTypeCollection import ContentTypeCollection
from office365.onedrive.drive import Drive
from office365.onedrive.driveCollection import DriveCollection
from office365.onedrive.listCollection import ListCollection
from office365.runtime.resource_path import ResourcePath


class Site(BaseItem):
    """The site resource provides metadata and relationships for a SharePoint site. """

    @property
    def columns(self):
        """The collection of columns under this site."""
        return self.properties.get('columns',
                                   ColumnDefinitionCollection(self.context,
                                                              ResourcePath("columns", self.resource_path)))

    @property
    def contentTypes(self):
        """The collection of content types under this site."""
        return self.properties.get('contentTypes',
                                   ContentTypeCollection(self.context,
                                                         ResourcePath("contentTypes", self.resource_path)))

    @property
    def lists(self):
        """The collection of lists under this site."""
        return self.properties.get('lists',
                                   ListCollection(self.context, ResourcePath("lists", self.resource_path)))

    @property
    def drive(self):
        """The default drive (document library) for this site."""
        return self.properties.get('drive',
                                   Drive(self.context, ResourcePath("drive", self.resource_path)))

    @property
    def drives(self):
        """The collection of drives under this site."""
        return self.properties.get('drives',
                                   DriveCollection(self.context, ResourcePath("drives", self.resource_path)))

    @property
    def sharepoint_ids(self):
        """Returns identifiers useful for SharePoint REST compatibility."""
        return self.properties.get('sharepointIds', None)

    @property
    def sites(self):
        """The collection of sites under this site."""
        from office365.onedrive.siteCollection import SiteCollection
        return self.properties.get('sites',
                                   SiteCollection(self.context, ResourcePath("sites", self.resource_path)))

    def set_property(self, name, value, persist_changes=True):
        super(Site, self).set_property(name, value, persist_changes)
        if name == "id" and self._resource_path.segment == "root":
            self._resource_path = ResourcePath(value, self._resource_path.parent)
        return self
