SSL_DIR := .ssl
BUILD_DIR := build

build:  # todo
	echo Building monobinary...

clear_build:
	rm -rvf $(BUILD_DIR)

cert: clear
	mkdir $(SSL_DIR)
#	openssl ecparam -genkey -name secp521r1 -noout -out ec512-key-pair.pem

clear_cert:
	rm -rvf $(SSL_DIR)

clear: clear_cert clear_build
