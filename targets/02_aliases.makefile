## 
## --- Aliases for targets in this Makefile ---
## 

# Define target aliases available both inside and outside a running REPRO
start:   start-image    ## Start a new container using the Docker image.
## 
clean:   clean-code     ## Delete artifacts from previous builds.
build:   build-code     ## Build custom code.
test:    test-code      ## Run tests on custom code.
package: package-code   ## Package custom code for distribution

# Define target aliases available only outside a running REPRO
ifndef IN_RUNNING_REPRO
## 
image:   build-image    ## Build the Docker image used to run this REPRO.
endif
