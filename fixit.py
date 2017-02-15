import yaml

def process_build_config(some_yaml):
    del some_yaml['metadata']['annotations']

if __name__ == '__main__':
    input = open('examples/swn-template-orig.yaml', 'r')
    output = open('examples/swt-script-out.yaml', 'w')

    the_yaml = yaml.load(input)

    list_of_kinds = []
    for openshift_object in the_yaml['objects']:
        list_of_kinds.append(openshift_object['kind'])


    for i in range(len(list_of_kinds)):

        ###### global remove metadata annotations
        del the_yaml['objects'][i]['metadata']['annotations']
        if 'generation' in the_yaml['objects'][i]['metadata']:
            del the_yaml['objects'][i]['metadata']['generation']

        ############deploymentConfigs
        # in DeploymentConfig get rid of spec:template:metadata:annotations
            # in template:spec:containers change the image value to just the image name not the URL
        if the_yaml['objects'][i]['kind'] == 'DeploymentConfig':
            del the_yaml['objects'][i]['spec']['template']['metadata']['annotations']
            lengthOfContainers = len(the_yaml['objects'][i]['spec']['template']['spec']['containers'])
            for j in range(lengthOfContainers):
                container_image = the_yaml['objects'][i]['spec']['template']['spec']['containers'][j]['image']
                first_slash = container_image.index('/')+1
                last_slash = container_image.index('/', first_slash)
                the_yaml['objects'][i]['spec']['template']['spec']['containers'][j]['image'] = container_image[first_slash+1:last_slash]

            # in triggers:imageChangeParams:from remove the namespace
            lengthOfTriggers = len(the_yaml['objects'][i]['spec']['triggers'])
            for j in range(lengthOfTriggers):
                if the_yaml['objects'][i]['spec']['triggers'][j]['type'] == 'ImageChange':
                    del the_yaml['objects'][i]['spec']['triggers'][j]['imageChangeParams']['from']['namespace']


        ###################

        ############ImageStreams
        # if ImageStream spec:tags:annotations has a key openshift.io/imported-from then remove everything inside spec and just put
            # a dockerImageRepository: <value of imported-from>
            # else the spec just becomes {}
        if the_yaml['objects'][i]['kind'] == 'ImageStream':
            annotations_count = len(the_yaml['objects'][i]['spec']['tags'])

            for j in range(annotations_count):
                if the_yaml['objects'][i]['spec']['tags'][j]['annotations'] is None:
                    the_yaml['objects'][i]['spec'] = {}
                elif 'openshift.io/imported-from' in the_yaml['objects'][i]['spec']['tags'][j]['annotations']:
                    imported_from = the_yaml['objects'][i]['spec']['tags'][j]['annotations']['openshift.io/imported-from']
                    the_yaml['objects'][i]['spec'] = {'dockerImageRepository', imported_from}
                else:
                    the_yaml['objects'][i]['spec'] = {}
        ###################

    output.write(yaml.dump(the_yaml))
    print(yaml.dump(the_yaml))
    input.close()
    output.close()