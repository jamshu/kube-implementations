kubectl apply -f filestore.yaml

kubectl patch storageclass filestore-csi --type=json -p="[{\"op\": \"add\", \"path\": \"/metadata/annotations/storageclass.kubernetes.io~1is-default-class\", \"value\": \"true\"}]"

kubectl patch storageclass standard-rwo --type=json -p="[{\"op\": \"add\", \"path\": \"/metadata/annotations/storageclass.kubernetes.io~1is-default-class\", \"value\": \"false\"}]"