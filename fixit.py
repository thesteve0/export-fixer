import yaml

def process_build_config(some_yaml):
    del some_yaml['metadata']['annotations']

if __name__ == '__main__':
    input = open('examples/swn-template-orig.yaml', 'r')

    the_yaml = yaml.load(input)

    # need to process a type or an item at a time.
    # Start with 'metada' 'annotation'
    # start with IS because sometimes they need the annotation

    list_of_kinds = []
    for openshift_object in the_yaml['objects']:
        list_of_kinds.append(openshift_object['kind'])

    # remove metadata annotations
    for i in range(len(list_of_kinds)):
       del the_yaml['objects'][i]['metadata']['annotations']



    print(the_yaml)