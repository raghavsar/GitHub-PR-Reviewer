# import base64
# from urllib.parse import urlparse
# content_str="CmZyb20gZGphbmdvLmNvbnRyaWIgaW1wb3J0IGFkbWluCmZyb20gLm1vZGVs\ncyBpbXBvcnQgQ3VycmVuY3ksIEN1cnJlbmN5RXhjaGFuZ2VSYXRlCgpjbGFz\ncyBDdXJyZW5jeUFkbWluKGFkbWluLk1vZGVsQWRtaW4pOgogICAgbGlzdF9k\naXNwbGF5ID0gWwogICAgICAgICJjb2RlIiwKICAgICAgICAibmFtZSIsCiAg\nICAgICAgInN5bWJvbCIsCiAgICBdCiAgICBzZWFyY2hfZmllbGRzID0gWwog\nICAgICAgICJjb2RlIiwKICAgICAgICAibmFtZSIsCiAgICAgICAgInN5bWJv\nbCIsCiAgICBdCgpjbGFzcyBDdXJyZW5jeUV4Y2hhbmdlUmF0ZUFkbWluKGFk\nbWluLk1vZGVsQWRtaW4pOgogICAgbGlzdF9kaXNwbGF5ID0gWwogICAgICAg\nICJzb3VyY2VfY3VycmVuY3kiLAogICAgICAgICJleGNoYW5nZWRfY3VycmVu\nY3kiLAogICAgICAgICJ2YWx1YXRpb25fZGF0ZSIsCiAgICAgICAgInJhdGVf\ndmFsdWUiXQogICAgCmFkbWluLnNpdGUucmVnaXN0ZXIoQ3VycmVuY3ksQ3Vy\ncmVuY3lBZG1pbikKYWRtaW4uc2l0ZS5yZWdpc3RlcihDdXJyZW5jeUV4Y2hh\nbmdlUmF0ZSxDdXJyZW5jeUV4Y2hhbmdlUmF0ZUFkbWluKQoKCg==\n"
#
# print(base64.b64decode(content_str).decode())

# def get_owner_and_repo(url):
#     passed_url = urlparse(url)
#     path_parts = passed_url.path.strip("/").split("/")
#     if len(path_parts) >=2 :
#         owner, repo = path_parts[0], path_parts[1]
#         return owner, repo
#     return None, None
# print(get_owner_and_repo("https://github.com/raghavsar/MyCurrency"))

from redis import Redis
r = Redis(host='localhost', port=6379)
print(r.ping())  # Should return True if Redis is reachable
