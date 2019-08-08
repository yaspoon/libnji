#include <stdio.h>
#include <stdlib.h>

#define EXPORT __attribute__((visibility("default")))

EXPORT void print_ptr(void *ptr)
{
	printf("printr_ptr ptr:%p\n", ptr);
}

EXPORT void print_ptr_jvm(void *ptr)
{
	printf("printr_ptr ptr:%p\n", ptr);
	if(ptr != NULL) {
		for(int i = 0; i < 10; i++) {
			printf("printr_ptr ptr[%d]:%p\n", i, ((void**)ptr)[i]);
		}
	}
}

int hidden(void *ptr)
{
	printf("hidden ptr:%p\n", ptr);
	return 1234;
}

struct libtest
{
	int value;
	int (*hidden)(void *);
};

EXPORT void get_ptr(void **ptr)
{
	struct libtest *lt = (struct libtest*)malloc(sizeof(struct libtest));
	lt->value = 1234;
	lt->hidden = hidden;
	*ptr = lt;
	printf("get_ptr lt:%p\n", lt);
	return;
}

EXPORT void put_ptr(void *ptr)
{
	printf("put_ptr ptr:%p\n", ptr);
	struct libtest *lt = (struct libtest*)ptr;
	printf("put_ptr lt->value:%d\n", lt->value);
	free(lt);
	return;
}
