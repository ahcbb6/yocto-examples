SUMMARY = "Hello Yocto Example Recipe"
LICENSE = "CLOSED"

SRC_URI += "file://hello_yocto.c"

do_compile(){
    ${CC} -o hello_yocto ../hello_yocto.c
}

do_install(){
    install -d ${D}${bindir}
    install -m 777 hello_yocto ${D}${bindir}/hello_yocto
}

