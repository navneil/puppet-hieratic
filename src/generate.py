import os
import string
import subprocess
import sys
import tempfile

current_dir = os.path.dirname(os.path.realpath(__file__))
resource_dir = os.path.normpath(current_dir + '/../resources/') + '/'

puppet_types = [line.strip() for line in open(resource_dir + 'typelist.txt')]
puppet_types.sort()

f = open(resource_dir + 'parameters.tmpl')
parameter_tmpl = string.Template(f.read())
f.close()

f = open(resource_dir + 'createblock.tmpl')
typedef_tmpl = string.Template(f.read())
f.close()

f = open(resource_dir + 'header.tmpl')
hieratic_class = f.read()
f.close()

hieratic_class += """\nclass hieratic (
  $global_enable = true,
"""

for puppet_type in puppet_types:
  type_label = puppet_type
  if type_label == 'class':
    type_label = 'classes'
  hieratic_class += parameter_tmpl.substitute(type=puppet_type, type_label_default=type_label)

hieratic_class += ") {\n\n"

for puppet_type in puppet_types:
  hieratic_class += typedef_tmpl.substitute(type=puppet_type) + "\n"

hieratic_class += "}"


# puppet-lint only works on files, so we write it to temp and return the result.
f = tempfile.NamedTemporaryFile()
f.write(hieratic_class)
devnull = open(os.devnull, 'w')
subprocess.call(['puppet-lint',f.name,'--fix'],
  stdout=devnull, stderr=devnull
)
f.seek(0)
hieratic_class = f.read()
f.close()


print hieratic_class
