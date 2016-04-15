FILES :=                            \
	.gitignore						\
	.travis.yml						\
	makefile						\
	apiary.apib						\
	IDB3.log						\
	models.html						\
	swecune/models.py 				\
	swecune/tests.py 			    \
	UML.pdf

models.html: models.py
	pydoc3 -w models

IDB3.log:
	git log > IDB3.log

check:
	@not_found=0;                                 \
    for i in $(FILES);                            \
    do                                            \
        if [ -e $$i ];                            \
        then                                      \
            echo "$$i found";                     \
        else                                      \
            echo "$$i NOT FOUND";                 \
            not_found=`expr "$$not_found" + "1"`; \
        fi                                        \
    done;                                         \
    if [ $$not_found -ne 0 ];                     \
    then                                          \
        echo "$$not_found failures";              \
        exit 1;                                   \
    fi;                                           \
    echo "success";

clean:
	rm -f  .coverage
	rm -f  *.pyc
	rm -f  *.tmp
	rm -rf __pycache__

config:
	git config -l

html: models.html

log: IDB1.log

status:
	make clean
	@echo
	git branch
	git remote -v
	git status