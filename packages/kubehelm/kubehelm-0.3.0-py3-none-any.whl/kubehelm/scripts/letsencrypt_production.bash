#!/usr/bin/env bash


kubectl apply -o json -f - <<EOF
apiVersion: cert-manager.io/v1
kind: ClusterIssuer
metadata:
  name: letsencrypt-prod
spec:
  acme:
    email: asim@asim.com
    server: https://acme-v02.api.letsencrypt.org/directory

    privateKeySecretRef:
      name: letsencrypt-prod-private-key

    solvers:
    - http01:
        ingress:
          class: nginx
EOF
