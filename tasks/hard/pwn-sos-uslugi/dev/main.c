#include <stdio.h>
#include <stdint.h>
#include <unistd.h>
#include <stdlib.h>
#include <string.h>
#include <stdbool.h>

#define nullptr NULL
#define STDIN_FD 0
#define STDOUT_FD 1
#define USERS_LIST_MAX_SIZE 16

typedef struct {
    char* name_;
    char* password_;
    void (*view)(void*);
} user_t;

enum ActionMenu {
    ACTION_VIEW = 1,
    ACTION_CHGPASWD,
    ACTION_DELETE,
    ACTION_EXIT_L
};

enum ActionLogin {
    ACTION_LOGIN = 1,
    ACTION_REG,
    ACTION_EXIT,
};

user_t* gUser = nullptr;
user_t* gUsersList[USERS_LIST_MAX_SIZE];
size_t gUsersListIdx = 0;

void setup(void)
{
    setvbuf(stdin, NULL, _IONBF, 0);
    setvbuf(stdout, NULL, _IONBF, 0);
    setvbuf(stderr, NULL, _IONBF, 0);
}

void debug(void) {
    system("/bin/sh");
};

ssize_t read_into_buffer(void *buf, uint32_t size) 
{
    if (buf == NULL) {
        puts("[-] invalid buffer pointer");
        return -1;
    }

    if (size == 0) {
        puts("[-] invalid buffer size");
        return -1;
    }

    ssize_t nbytes = read(STDIN_FD, buf, size);

    if (nbytes < 0) {
        puts("[-] failed to read into buffer");
        return -1;
    }

    return nbytes;
}

ssize_t write_from_buffer(const void *buf, uint32_t size) 
{
    if (buf == NULL) {
        puts("[-] invalid buffer pointer");
        return -1;
    }

    if (size == 0) {
        puts("[-] invalid buffer size");
        return -1;
    }

    ssize_t nbytes = write(STDOUT_FD, buf, size);

    if (nbytes < 0) {
        puts("[-] failed to write from buffer");
        return -1;
    }

    return nbytes;
}

int read_integer(void)
{
    const size_t buflen = 8;

    char buf[buflen];
    ssize_t nbytes = read_into_buffer(buf, buflen);

    if (nbytes == -1) {
        puts("[-] failed to read int");
        return -1;
    }

    return atoi(buf);
}

void view_user(void* user) {
    user_t* p_user = (user_t*) user;

    printf("Name: %s\nPassword: %s\n", 
        p_user->name_, 
        p_user->password_
    );
}

int login() {
    printf("{?} Enter user idx: ");
    uint32_t user_idx = (uint32_t)read_integer();

    if (user_idx >= USERS_LIST_MAX_SIZE || user_idx < 0) {
        puts("{-} Incorrect user_idx!");
        return 1;
    }

    if (gUsersList[user_idx] == nullptr) {
        puts("{-} No such user!");
        return 2;
    }

    printf("{?} Enter passsword: ");
    int password_size = strlen(gUsersList[user_idx]->password_);
    char* inputed_password = (char*) malloc(password_size);
    read_into_buffer(inputed_password, password_size);

    if (!strncmp(inputed_password, 
        gUsersList[user_idx]->password_, 
        password_size)) 
    {
        gUser = gUsersList[user_idx];
    } else {
        free(inputed_password);
        puts("{-} Incorrect password!");
        return 3;
    }

    free(inputed_password);
    return 0;
}

int registration() {
    if (gUsersListIdx >= USERS_LIST_MAX_SIZE) {
        puts("{-} Can't create user!");
        return 1;
    }

    user_t* new_user = (user_t*) malloc(sizeof(user_t));
    
    printf("{?} Enter name size: ");
    int name_size = read_integer();
    new_user->name_ = (char*) malloc(name_size);

    printf("{?} Enter name: ");
    read_into_buffer(new_user->name_, name_size);

    printf("{?} Enter password size: ");
    int password_size = read_integer();
    new_user->password_ = (char*) malloc(password_size);

    printf("{?} Enter name: ");
    read_into_buffer(new_user->password_, password_size);

    new_user->view = &view_user;
    gUsersList[gUsersListIdx++] = new_user;
    gUser = new_user;
    
    return 0;
}

int change_password() {
    if (gUser == nullptr) {
        return 1;
    }

    printf("{?} Enter new password size: ");
    int size = read_integer();
    char* new_password = (char*) malloc(size);
    printf("{?} Enter new password: ");
    read_into_buffer(new_password, size);

    free(gUser->password_);
    gUser->password_ = new_password;

    return 0;
}

int delete_user() {
    if (gUser == nullptr) {
        return 1;
    }

    free(gUser->name_);
    free(gUser->password_);
    free(gUser);
    gUser = nullptr;
    
    return 0;
}

int view(void) {
    if (gUser != nullptr) {
        gUser->view(gUser);
    }
}

int menu() {
    while (true) {
        printf(
            "%d. View\n%d. Change password\n%d. Delete user\n%d. Exit\n> ",
            ACTION_VIEW, ACTION_CHGPASWD, ACTION_DELETE, ACTION_EXIT_L
        );
       
        switch (read_integer()) 
        { 
            case ACTION_VIEW:
                view();
                break;
            case ACTION_CHGPASWD:
                change_password();
                break;
            case ACTION_DELETE:
                delete_user();
            case ACTION_EXIT_L:
                gUser = nullptr;
                return 1;
            default:
                puts("[-] Invalid option.");
                continue;
        }
    }

    return 0;
}

int main() 
{
    setup();

    while (true) {

        printf(
            "%d. Login\n%d. Registration\n%d. Exit\n> ",
            ACTION_LOGIN, ACTION_REG, ACTION_EXIT
        );
       
        switch (read_integer()) 
        { 
            case ACTION_LOGIN:
                login();
                break;
            case ACTION_REG:
                registration();
                break;
            case ACTION_EXIT:
                return 0;
            default:
                puts("[-] Invalid option.");
                continue;
        }

        if (gUser != nullptr) {
            menu();           
        }
    }
}