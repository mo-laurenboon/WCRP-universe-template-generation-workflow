# import os
# import re

# repo_path = './'  # Update this with your repo path

# for root, _, files in os.walk(repo_path):
#     for file in files:
#         if file.endswith(".py"):
#             file_path = os.path.join(root, file)

#             with open(file_path, "r") as f:
#                 content = f.read()

#             modified = False

#             # Ensure import statement is present
#             if "from cmipld.utils.checksum import version" not in content:
#                 content = content.replace(
#                     "from cmipld.utils.ldparse import *",
#                     "from cmipld.utils.ldparse import *\nfrom cmipld.utils.checksum import version",
#                 )
#                 modified = True

#             # Modify summary assignment
#             # content, count1 = re.subn(
#             #     r"(summary\s*=\s*name_extract\(data\))",
#             #     r"summary = version(\1, me, location)",
#             #     content,
#             # )

#             # # Ensure write function uses the modified summary
      
            
            
#             content, count2= re.subn(
#                 r"cmipld\.utils\.io\.wjsn\(\s*\w+\s*,[^\)]+\)",
#                 "location = f'{repopath}/{reponame}_{me}.json'\n    summary = version(summary, me, location.split("/")[-1])\n    cmipld.utils.io.wjsn(summary,location)",
#                 content
#             )
            

#             if modified or count2:
#                 with open(file_path, "w") as f:
#                     f.write(content)
#                 print(f"Updated {file_path}")
