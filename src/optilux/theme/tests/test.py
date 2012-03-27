import unittest2 as unittest
import transaction

from optilux.theme.testing import OPTILUX_THEME_INTEGRATION_TESTING
from optilux.theme.testing import OPTILUX_THEME_FUNCTIONAL_TESTING

from plone.testing.z2 import Browser
from plone.app.testing import SITE_OWNER_NAME
from plone.app.testing import SITE_OWNER_PASSWORD

from zope.component import getUtility
from Products.CMFCore.utils import getToolByName

from plone.registry.interfaces import IRegistry
from plone.app.theming.interfaces import IThemeSettings

class TestSetup(unittest.TestCase):
    
    layer = OPTILUX_THEME_INTEGRATION_TESTING
    
    def setUp(self):
        self.app = self.layer['app']
        self.portal = self.layer['portal']
        self.qi_tool = getToolByName(self.portal, 'portal_quickinstaller')
    
    def test_product_is_installed(self):
        """ Validate that our products GS profile has been run and the product 
            installed
        """
        pid = 'optilux.theme'
        installed = [p['id'] for p in self.qi_tool.listInstalledProducts()]
        self.assertTrue(pid in installed,
                        'package appears not to have been installed')
    
    def test_css_registry_configured(self):
        portal = self.layer['portal']
        cssRegistry = getToolByName(portal, 'portal_css')
        self.assertTrue("++theme++optilux.theme/stylesheets/main.css" 
                in cssRegistry.getResourceIds()
            )
        self.assertTrue("++theme++optilux.theme/stylesheets/iefixes.css"
                in cssRegistry.getResourceIds()
            )
    
    def test_theme_configured(self):
        registry = getUtility(IRegistry)
        settings = registry.forInterface(IThemeSettings)
        self.assertEqual(settings.enabled, True)
        self.assertEqual(settings.rules, 
                "/++theme++optilux.theme/rules.xml"
            )
        self.assertEqual(settings.absolutePrefix,
                "/++theme++optilux.theme"
            )

class TestRendering(unittest.TestCase):
    
    layer = OPTILUX_THEME_FUNCTIONAL_TESTING
    
    def test_render_plone_page(self):
        app = self.layer['app']
        portal = self.layer['portal']
        
        transaction.commit()
        
        browser = Browser(app)
        
        browser.open(portal.absolute_url())
        self.assertTrue('<div id="wrapper">' in browser.contents)
    
    def test_render_zmi_page(self):
        app = self.layer['app']
        portal = self.layer['portal']
        
        transaction.commit()
        
        browser = Browser(app)
        browser.addHeader('Authorization', 'Basic %s:%s' % (SITE_OWNER_NAME, SITE_OWNER_PASSWORD,))
        
        browser.open(portal.absolute_url() + '/manage_main')
        
        self.assertFalse('<div id="wrapper">' in browser.contents)
