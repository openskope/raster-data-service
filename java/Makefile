all: build test install

clean:
	mvn clean

build:
	mvn compile
	
package: build
	mvn package
	cp target/timeseries-service-0.2.1.jar ${REPRO_MNT}/service/

test: package
	make -C ../service run &
	make -C ../javascript install test
