# -*- coding: utf-8 -*-

#******************************************************************************
#
# Metatools
# ---------------------------------------------------------
# Metadata browser/editor
#
# Copyright (C) 2011 NextGIS (info@nextgis.ru)
#
# This source is free software; you can redistribute it and/or modify it under
# the terms of the GNU General Public License as published by the Free
# Software Foundation; either version 2 of the License, or (at your option)
# any later version.
#
# This code is distributed in the hope that it will be useful, but WITHOUT ANY
# WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS
# FOR A PARTICULAR PURPOSE.  See the GNU General Public License for more
# details.
#
# A copy of the GNU General Public License is available on the World Wide Web
# at <http://www.gnu.org/copyleft/gpl.html>. You can also obtain it by writing
# to the Free Software Foundation, Inc., 59 Temple Place - Suite 330, Boston,
# MA 02111-1307, USA.
#
#******************************************************************************

from PyQt4.QtGui import *
from PyQt4.QtCore import *
from PyQt4.QtXml import *

import os, codecs

class LicenseTemplateManager:
  LICENSE_SUBFOLDER = 'templates/license'
  LICENSE_EXT = '.xml'

  def __init__( self, basePluginPath ):
    self.basePluginPath = str( basePluginPath )

  def getLicenseTemplatesPath( self ):
    return os.path.join( self.basePluginPath, self.LICENSE_SUBFOLDER )

  def getTemplateFilePath( self, templateName ):
    return os.path.join( self.getLicenseTemplatesPath(), str( templateName ) + self.LICENSE_EXT )

  def getTemplateList( self ):
    templatesList = []
    for filename in os.listdir( self.getLicenseTemplatesPath() ):
      name, ext = os.path.splitext( filename )
      if ext == self.LICENSE_EXT:
        templatesList.append( name )
    return templatesList

  def loadLicenseTemplate( self, templateName ):
    # TODO: more cheks on struct!
    licenseTemplate = LicenseTemplate()
    templateFile = QFile( self.getTemplateFilePath( templateName.toUtf8() ) )

    xmlTemplate = QDomDocument()
    xmlTemplate.setContent( templateFile )

    root = xmlTemplate.documentElement()
    nameElement = root.elementsByTagName( "Name" ).at( 0 )
    versionElement = root.elementsByTagName( "Version" ).at( 0 )
    descriptionElement = root.elementsByTagName( "Description" ).at( 0 )

    licenseTemplate.name = nameElement.childNodes().at( 0 ).nodeValue()
    licenseTemplate.version = versionElement.childNodes().at( 0 ).nodeValue()
    licenseTemplate.description = descriptionElement.childNodes().at( 0 ).nodeValue()

    return licenseTemplate

  def saveLicenseTemplate( self, licenseTemplate ):
    xmlTemplate = QDomDocument()

    # create root
    root = xmlTemplate.createElement( "LicenseTemplate" )
    xmlTemplate.appendChild( root )

    # set name
    element = xmlTemplate.createElement( "Name" )
    textNode = xmlTemplate.createTextNode( licenseTemplate.name )
    element.appendChild( textNode )
    root.appendChild( element )

    # set version
    element = xmlTemplate.createElement( "Version" )
    textNode = xmlTemplate.createTextNode( licenseTemplate.version )
    element.appendChild( textNode )
    root.appendChild( element )

    # set desc
    element = xmlTemplate.createElement( "Description" )
    textNode = xmlTemplate.createTextNode( licenseTemplate.description )
    element.appendChild( textNode )
    root.appendChild( element )

    templateFile = codecs.open( self.getTemplateFilePath( licenseTemplate.name.toUtf8() ), "w", encoding="utf-8" )
    templateFile.write( unicode( xmlTemplate.toString().toUtf8(), "utf-8" ) )
    templateFile.close()

  def removeLicenseTemplate( self, templateName ):
    os.remove( self.getTemplateFilePath( templateName ) )

class LicenseTemplate:
  def __init__( self, name = None, version = None, description = None ):
    self.name = name
    self.version = version
    self.description = description

  def stringRepresentation( self ):
    return self.name + '::' + self.version + '::' + self.description
