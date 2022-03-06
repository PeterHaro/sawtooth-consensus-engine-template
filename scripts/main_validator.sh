
echo "starting keys generation" &&
sawadm keygen validator-1 &&
sawadm keygen validator-2 &&
sawadm keygen validator-3 &&
sawadm keygen validator-4 &&
sawadm keygen validator-5 &&
sawadm keygen validator-6 &&
sawadm keygen validator-7 &&
sawadm keygen validator-8 &&
sawadm keygen validator-9 &&
sawadm keygen validator-10 &&
sawadm keygen &&
echo "done with keys generation"

set -x
sawset genesis \
  -k /etc/sawtooth/keys/validator.priv \
  -o config-genesis.batch &&
sawset proposal create \
  -k /etc/sawtooth/keys/validator.priv \
  sawtooth.consensus.algorithm.name=custom-consensus \
  sawtooth.consensus.algorithm.version=0.1 \
  sawtooth.consensus.custom_consensus.example=example_value \
  -o config.batch &&
sawadm genesis \
  config-genesis.batch \
  config.batch &&
mv /etc/sawtooth/keys/validator-* /shared_keys &&
cat /etc/sawtooth/keys/validator.pub
sawtooth-validator -vvv \
  --endpoint tcp://validator-0:8800 \
  --bind component:tcp://eth0:4004 \
  --bind network:tcp://eth0:8800 \
  --bind consensus:tcp://eth0:5050 \
  --peering static \
  --scheduler parallel \
  --maximum-peer-connectivity 10
set +x