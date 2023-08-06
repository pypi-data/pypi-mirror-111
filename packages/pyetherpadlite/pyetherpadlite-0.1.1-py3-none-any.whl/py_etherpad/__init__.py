#!/usr/bin/env python
"""Module to talk to EtherpadLite API."""

import json
try:
    import urllib.parse as urllib_parse
    import urllib.error as urllib_error
    import urllib.request as urllib_request
    import urllib.request as build_opener
except ImportError:
    import urllib as urllib_parse
    import urllib2 as urllib_error
    import urllib2 as urllib_request
    import urllib2 as build_opener

class EtherpadLiteClient:
    """Client to talk to EtherpadLite API."""
    API_VERSION = "1.2.13"  # TODO probably 1.1 sometime soon

    CODE_OK = 0
    CODE_INVALID_PARAMETERS = 1
    CODE_INTERNAL_ERROR = 2
    CODE_INVALID_FUNCTION = 3
    CODE_INVALID_API_KEY = 4
    TIMEOUT = 20

    apiKey = ""
    baseUrl = "http://localhost:9001/api"

    def __init__(self, apiKey=None, baseUrl=None):
        if apiKey:
            self.apiKey = apiKey

        if baseUrl:
            self.baseUrl = baseUrl

    def call(self, function, arguments=None):
        """Create a dictionary of all parameters"""
        url = '%s/%s/%s' % (self.baseUrl, self.API_VERSION, function)

        params = arguments or {}
        params.update({'apikey': self.apiKey})
        data = urllib_parse.urlencode(params, True)
        data = data.encode('utf-8')

        try:
            opener = build_opener.build_opener()
            request = urllib_request.Request(url=url, data=data)
            response = opener.open(request, timeout=self.TIMEOUT)
            #result = json.loads(response.readall().decode('utf-8'))
            #import pdb; pdb.set_trace()
            result = response.read().decode('utf-8')
            response.close()
        except urllib_error.HTTPError:
            raise

        #result = json.loads(result['message'])
        result = json.loads(result)
        if result is None:
            raise ValueError("JSON response could not be decoded")

        return self.handleResult(result)

    def handleResult(self, result):
        """Handle API call result"""
        if 'code' not in result:
            raise Exception("API response has no code")
        if 'message' not in result:
            raise Exception("API response has no message")

        if 'data' not in result:
            result['data'] = None

        if result['code'] == self.CODE_OK:
            return result['data']
        elif result['code'] == self.CODE_INVALID_PARAMETERS or result['code'] == self.CODE_INVALID_API_KEY:
            raise ValueError(result['message'])
        elif result['code'] == self.CODE_INTERNAL_ERROR:
            raise Exception(result['message'])
        elif result['code'] == self.CODE_INVALID_FUNCTION:
            raise Exception(result['message'])
        else:
            raise Exception("An unexpected error occurred whilst handling the response")

    # GROUPS
    # Pads can belong to a group. There will always be public pads that do not belong to a group (or we give this group the id 0)

    def createGroup(self):
        """creates a new group"""
        return self.call("createGroup")

    def createGroupIfNotExistsFor(self, groupMapper):
        """this functions helps you to map your application group ids to etherpad lite group ids"""
        return self.call("createGroupIfNotExistsFor", {
            "groupMapper": groupMapper
        })

    def deleteGroup(self, groupID):
        """deletes a group"""
        return self.call("deleteGroup", {
            "groupID": groupID
        })

    def listPads(self, groupID):
        """returns all pads of this group"""
        return self.call("listPads", {
            "groupID": groupID
        })

    def createGroupPad(self, groupID, padName, text=''):
        """creates a new pad in this group"""
        params = {
            "groupID": groupID,
            "padName": padName,
        }
        if text:
            params['text'] = text
        return self.call("createGroupPad", params)

    def listAllGroups(self):
        """returns list of all existing groups"""
        return self.call("listAllGroups")

    # AUTHORS
    # Theses authors are bind to the attributes the users choose (color and name).

    def createAuthor(self, name=''):
        """creates a new author"""
        params = {}
        if name:
            params['name'] = name
        return self.call("createAuthor", params)

    def createAuthorIfNotExistsFor(self, authorMapper, name=''):
        """this functions helps you to map your application author ids to etherpad lite author ids"""
        params = {
            'authorMapper': authorMapper
        }
        if name:
            params['name'] = name
        return self.call("createAuthorIfNotExistsFor", params)

    def listPadsOfAuthor(self, authorID):
        """returns the ids of all pads this author has edited"""
        return self.call("listPadsOfAuthor", {
            "authorID": authorID
        })

    def getAuthorName(self, authorID):
        """returns the name of the Author"""
        return self.call("getAuthorName", {
            "authorID": authorID
        })

    # SESSIONS
    # Sessions can be created between a group and a author. This allows
    # an author to access more than one group. The sessionID will be set as
    # a cookie to the client and is valid until a certain date.

    def createSession(self, groupID, authorID, validUntil):
        """creates a new session"""
        return self.call("createSession", {
            "groupID": groupID,
            "authorID": authorID,
            "validUntil": validUntil
        })

    def deleteSession(self, sessionID):
        """deletes a session"""
        return self.call("deleteSession", {
            "sessionID": sessionID
        })

    def getSessionInfo(self, sessionID):
        """returns informations about a session"""
        return self.call("getSessionInfo", {
            "sessionID": sessionID
        })

    def listSessionsOfGroup(self, groupID):
        """returns all sessions of a group"""
        return self.call("listSessionsOfGroup", {
            "groupID": groupID
        })

    def listSessionsOfAuthor(self, authorID):
        """returns all sessions of an author"""
        return self.call("listSessionsOfAuthor", {
            "authorID": authorID
        })

    # PAD CONTENT
    # Pad content can be updated and retrieved through the API

    def getText(self, padID, rev=None):
        """returns the text of a pad"""
        params = {"padID": padID}
        if rev is not None:
            params['rev'] = rev
        return self.call("getText", params)

    def setText(self, padID, text):
        """sets the text of a pad"""
        return self.call("setText", {
            "padID": padID,
            "text": text
        })
    
    def appendText(self, padID, text):
        """appends the text to a pad"""
        return self.call("appendText", {
            "padID": padID,
            "text": text
        })

    # introduced with pull request merge
    def getHtml(self, padID, rev=None):
        """returns the html of a pad"""
        params = {"padID": padID}
        if rev is not None:
            params['rev'] = rev
        return self.call("getHTML", params)

    def setHtml(self, padID, html):
        """sets the text of a pad from html"""
        return self.call("setHTML", {
            "padID": padID,
            "html": html
        })
    
    def getAttributePool(self, padID):
        """returns the attribute pool of a pad"""
        return self.call("getAttributePool", {
            "padID": padID
        })

    def getRevisionChangeset(self, padID, rev=None):
        """returns the changeset at a given revision, or last revision if rev is not defined"""
        params = {"padID": padID}
        if rev is not None:
            params['rev'] = rev
        return self.call("getRevisionChangeset", params)

    def createDiffHTML(self, padID, startRev, endRev):
        """returns an object of diffs from 2 points in a pad"""
        return self.call("createDiffHTML", {
            "padID": padID,
            "startRev": startRev,
            "endRev": endRev
        })

    def restoreRevision(self, padId, rev):
        """Restores revision from past as new changeset"""
        return self.call("restoreRevision", {
            "padId": padId,
            "rev": rev
        })

    # CHAT

    def getChatHistory(self, padID, start = None, end = None):
        """returns a part of the chat history, when start and end are given or the whole chat histroy, when no extra parameters are given"""
        params = {"padID": padID}
        if start is not None and end is not None:
            params['start'] = start
            params['end'] = end        
        return self.call("getRevisionChangeset", params) 

    # PAD
    # Group pads are normal pads, but with the name schema
    # GROUPID$PADNAME. A security manager controls access of them and its
    # forbidden for normal pads to include a  in the name.

    def createPad(self, padID, text=''):
        """creates a new pad"""
        params = {
            "padID": padID,
        }
        if text:
            params['text'] = text
        return self.call("createPad", params)

    def getRevisionsCount(self, padID):
        """returns the number of revisions of this pad"""
        return self.call("getRevisionsCount", {
            "padID": padID
        })

    def padUsersCount(self, padID):
        """returns the number of users currently editing this pad"""
        return self.call("padUsersCount", {
            "padID": padID
        })

    def getLastEdited(self, padID):
        """returns the time the pad was last edited as a Unix timestamp"""
        return self.call("getLastEdited", {
            "padID": padID
        })

    def deletePad(self, padID):
        """deletes a pad"""
        return self.call("deletePad", {
            "padID": padID
        })

    def getReadOnlyID(self, padID):
        """returns the read only link of a pad"""
        return self.call("getReadOnlyID", {
            "padID": padID
        })

    def listAuthorsOfPad(self, padID):
        """returns the ids of all authors who've edited this pad"""
        return self.call("listAuthorsOfPad", {
            "padID": padID
        })

    def setPublicStatus(self, padID, publicStatus):
        """sets a boolean for the public status of a pad"""
        return self.call("setPublicStatus", {
            "padID": padID,
            "publicStatus": publicStatus
        })

    def getPublicStatus(self, padID):
        """return true of false"""
        return self.call("getPublicStatus", {
            "padID": padID
        })

    def setPassword(self, padID, password):
        """returns ok or a error message"""
        return self.call("setPassword", {
            "padID": padID,
            "password": password
        })

    def isPasswordProtected(self, padID):
        """returns true or false"""
        return self.call("isPasswordProtected", {
            "padID": padID
        })

    # PADS
    
    def listAllPads(self):
        """returns list of all pads on this epl instance"""
        return self.call("listAllPads")