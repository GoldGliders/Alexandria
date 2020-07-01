user = {
    "userid":       "",  #str
    "bookmarks":    [],
    "favolib":      [],
    "options":      {},
    "history":      [],
    "context":      "",  #str
}

bookmeta = {
    "isbn":         0,   #int
    "title":        "",  #str
    "subtitle":     "",  #str
    "author":       "",  #str
    "page":         "",  #str
    "image":        "",  #str
    "publisher":    "",  #str
    "publishdate":  "",  #str
}

book_doc = {
    "timestamp":    0,   #int
    "bookmeta":     bookmeta,
}

library = {
    "timestamp":    0,   #int
    "formal":       "",  #str
    "systemid":     "",  #str
}
