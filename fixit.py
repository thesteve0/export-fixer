import yaml

if __name__ == '__main__':
    input = open('examples/molw-orig.yaml', 'r')
    output = open('examples/molw-out.yaml', 'w')

    the_yaml = yaml.load(input)


    for i in range(len(the_yaml['objects'])):
        print("I am on:  " + str(i))
        ###### global
        # remove metadata annotations
        if 'annotations' in the_yaml['objects'][i]['metadata']:
            del the_yaml['objects'][i]['metadata']['annotations']
        if 'generation' in the_yaml['objects'][i]['metadata']:
            del the_yaml['objects'][i]['metadata']['generation']
        del the_yaml['objects'][i]['status']

        ############deploymentConfigs
        # in DeploymentConfig get rid of spec:template:metadata:annotations
            # in template:spec:containers change the image value to just the image name not the URL
        if the_yaml['objects'][i]['kind'] == 'DeploymentConfig':
            if 'annotations' in the_yaml['objects'][i]['spec']['template']['metadata']:
                del the_yaml['objects'][i]['spec']['template']['metadata']['annotations']
            lengthOfContainers = len(the_yaml['objects'][i]['spec']['template']['spec']['containers'])

            # this logic is all wrong. There seems to be at least 3 types of strings here
            # image: 172.30.195.74:5000/swn/swn@sha256:62be9dc33b8aaeced1f783f3e9ba5297b2cdd0a7c53a4607982a76248be53661
            # image: winsent/geoserver@sha256:118d6211fdd51dd9030fae20afd6681ccb6188b1d14c7703f02eb422fa2a3b3d

            for j in range(lengthOfContainers):
                container_image = the_yaml['objects'][i]['spec']['template']['spec']['containers'][j]['image']
                if container_image[0:2].isdigit():
                    first_slash = container_image.index('/')+1
                    last_slash = container_image.index('/', first_slash)
                    at_symbol = container_image.index('@')
                    the_yaml['objects'][i]['spec']['template']['spec']['containers'][j]['image'] = container_image[last_slash+1:at_symbol]

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
                    the_yaml['objects'][i]['spec'] = {'dockerImageRepository': imported_from}
                else:
                    the_yaml['objects'][i]['spec'] = {}
        ###################

        ###########Routes
        if the_yaml['objects'][i]['kind'] == 'Route':
            # Remove the host fields
            if 'host' in the_yaml['objects'][i]['spec']:
                del the_yaml['objects'][i]['spec']['host']
        #################

        #################PVC

        if the_yaml['objects'][i]['kind'] == 'PersistentVolumeClaim':
            # remove the volume and tell people to hand edit the volume size they want
            if 'volumeName' in the_yaml['objects'][i]['spec']:
                del the_yaml['objects'][i]['spec']['volumeName']
        ####################


    output.write(yaml.dump(the_yaml))
    print(yaml.dump(the_yaml))
    input.close()
    output.close()