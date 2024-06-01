"""
portalQuickDelete.py
Creator: Tanner Hammond
Date: May 31, 2024
Description: A script for quickly removing items in ArcGIS Portal.
"""


#Input Parameters
portal = '' #URL, https:// automatically added.
username = ''
password = ''

owner = '' 
title = ''
type_ = ''

#MAIN
import arcgis
from arcgis import GIS

print('WARNING: This script will remove any items that are returned from gis.content.search.\nPut no value for any part of the query you will not be using.\n')

#Build Query
query = ''
if title != '':
    query = query + 'title: ' + title
if type_ != '':
    query = qury + 'type: ' + type_
elif type_ != '' and query != '':
    query = query + ', type: ' + type_
if owner != '':
    query = query + 'owner: ' + owner
elif owner != '' and query != '':
    query = query + ', owner: ' + owner

#Confirm
confirm = input(f'To confirm you would like to delete items matching the following query, type "YES".\nQuery: "{query}" \nConfirm: ')

#Login
print(f'Logging in to {portal} ...')
portal = 'https://' + portal
gis = GIS(portal, username, password)
print(f'Successfully logged in to: {portal} as {username}')

#Execute
if confirm == 'YES' and query == '':
    raise Exception('No query specified.')
elif confirm == 'YES':
    idList = []
    content = gis.content.search(query=query)
    index = 0
    for  item in content:
        id = content[index].id
        idList.append(id)
        index += 1
    #Delete
    for item in idList:
        o = gis.content.get(item)
        o.delete()
else:
    raise Exception('Confirm failed. Not executed.')

#Print Output
if len(content) == 0:
    raise Exception('No items found with the query provided.')
else:
    print('Items Deleted:')
    index = 0
    for item in content:
         print(f'{index + 1}. {content[index].title} \t {idList[index]}')
