# export-fixer
Getting the output from oc export to work as a template

## Assumptions
You already have oc command line tool installed and you have a project set up in OpenShift.
You want to export that project to another project or a different cluster

## Installation 
This was written with Python 3.5 and not tested with any other versions. Would love to 
know if it works for you with different versions. 

You need to install the PyYAML extension to use this. 
Follow the instructions in the [PyYAML documentation](http://pyyaml.org/wiki/PyYAMLDocumentation).
 
 ## Usage
     oc export bc,dc,svc,is,route --as-template=myapp >> my-orig-template.yml
 * Download the python file fixit.py
 * Edit the input name to match the file name above and put in an output file name
 * Run the script
 
 `oc new-app -f new-file-name.yml`
 
 ## Possible enhancements
 1. Allow passing in of filenames from commandline (Highly Likely)
 2. Use JSON rather YAML as file format so no need to install anything before using the script
  
 ## Help needed
 Please send me more before and after (or just the before outputs) so I can keep making sure 
 I cover all the use cases
  
 File a bug report in Kubernetes so they fix this upstream. 
 