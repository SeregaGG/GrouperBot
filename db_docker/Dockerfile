FROM mongo:3.6.8

COPY dump/ /tmp/dump/

CMD mongod --fork --logpath /var/log/mongodb.log; \
    mongorestore /tmp/dump/; \
    mongod --shutdown; \
    docker-entrypoint.sh mongod