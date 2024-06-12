from python_terraform import Terraform
import os
import subprocess

root_dir = './terraform_scripts'
total_scripts = 0
valid_scripts = 0
print(os.walk(root_dir))

for dirpath, dirnames, filenames in os.walk(root_dir):
    for filename in filenames:
        if filename.endswith('.tf'):
            total_scripts += 1
            tf = Terraform(working_dir=dirpath)
            return_code, stdout, stderr = tf.init(capture_output=False)
            return_code, stdout, stderr = tf.apply(skip_plan=True, capture_output=False)
            if return_code == 0:
                return_code, stdout, stderr = tf.destroy(force=True, capture_output=False)
                if return_code == 0:
                    valid_scripts += 1

validity_ratio = valid_scripts / total_scripts if total_scripts > 0 else 0
print(f'Validity ratio: {validity_ratio}', total_scripts)