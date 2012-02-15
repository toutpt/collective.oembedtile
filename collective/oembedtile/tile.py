from zope import interface
from zope import schema
from plone import tiles
from Products.Five.browser.pagetemplatefile import ViewPageTemplateFile

class IOEmbedTile(interface.Interface):
    """IOEmbed tile schema"""
    
    oembed_url = schema.URI(title=u"URL",
                     required=True)

    maxwidth = schema.Int(title=u"max width",
                          required=False)

    maxheight = schema.Int(title=u"Max height",
                           required=False)

class OEmbedTile(tiles.PersistentTile):
    """OEmebed tile implementation"""

    interface.implements(IOEmbedTile) 

    def __call__(self):
        import pdb;pdb.set_trace()
        return self.get_embed()

    def get_embed(self):
        client = component.queryMultiAdapter((self.context, self.request),
                                    name="collective.oembed.superconsumer")
        client.update()
        kwargs = {}
        if self.data.maxwidth:
            kwargs['maxwidth'] = self.data.maxwidth
        if self.data.maxheight:
            kwargs['maxheight'] = self.data.maxheight
        return client.get_embed(self.data.oembed_url, **kwargs)


from zope.component import adapter
from zope.lifecycleevent.interfaces import IObjectModifiedEvent
from plone.tiles.interfaces import ITile


@adapter(ITile, IObjectModifiedEvent)
def notifyModified(tile, event):
    # make sure the page's modified date gets updated
    tile.__parent__.notifyModified()
