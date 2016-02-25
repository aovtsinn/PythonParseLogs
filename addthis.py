import os

def humanize(bytes):
	if bytes < 1024:
		return "%d B" % bytes
	elif bytes < 1024 ** 2:
		return "%d kB" % (bytes/1024)
	elif bytes < 1024 ** 3:
		return "%d MB" % (bytes/1024 ** 2)
	else:
		return "%d GB" % (bytes / 1024 ** 3)

for filename in os.listdir("."):
	mode, inode, device, nlink, uid, gid, size, atime, mtime, ctime = os.stat(filename)
	print filename, humanize(size)
