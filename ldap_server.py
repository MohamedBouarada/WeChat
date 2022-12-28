import ldap
import hashlib
from base64 import b64encode
from dotenv.main import load_dotenv
import os
#cn or uid

class LdapServer():

    ldap_server = "ldap://localhost:389"  # host address
    ldap_ou = "People"  # organization unit
    

    # admin domain
    LDAP_ADMIN_DN = "cn=admin,dc=med-bouarada,dc=com"
    LDAP_ADMIN_PWD = ""

    def __init__(self, admin_pwd):
        self.LDAP_ADMIN_PWD = admin_pwd

    def login(self, username, password):
        self.username = username
        self.password = password

        # organization user domain
        user_dn = "cn=" + self.username +",ou=" + \
            self.ldap_ou + ",dc=med-bouarada,dc=com"

        print(user_dn)

        # base domain
        LDAP_BASE_DN ="ou=" + self.ldap_ou + ",dc=med-bouarada,dc=com"

        # start connection
        ldap_client = ldap.initialize(self.ldap_server)
        # search for specific user
        search_filter = "cn=" + self.username

        try:
            # if authentication successful, get the full user data
            ldap_client.bind_s(user_dn, self.password)
            result = ldap_client.search_s(
                LDAP_BASE_DN, ldap.SCOPE_SUBTREE, search_filter)

            # return user data
            ldap_client.unbind_s()
            print(result)
            return None
        except ldap.INVALID_CREDENTIALS:
            ldap_client.unbind()
            print("Wrong username or password..")
            return "Wrong username or password.."
        except ldap.SERVER_DOWN:
            print("Server is down at the moment, please try again later!")
            return "Server is down at the moment, please try again later!"
        except ldap.LDAPError:
            ldap_client.unbind_s()
            print("Authentication error!")
            return "Authentication error!"

    def register(self,user):
        # base domain
        LDAP_BASE_DN = "ou=" + self.ldap_ou + ",dc=med-bouarada,dc=com"
        # home directory
        HOME_DIRECTORY = "/home/users"

        # new user domain
        dn = 'cn=' + user['username'] + ',' + LDAP_BASE_DN
        home_dir = HOME_DIRECTORY + '/' + user['username']
        gid = user['group_id']

        # encoding password using md5 hash function
        hashed_pwd = hashlib.md5(user['password'].encode("UTF-8"))


        entry = []
        entry.extend([
            ('objectClass', [b'inetOrgPerson',
                             b'posixAccount', b'top']),
            ('uid', user['username'].encode("UTF-8")),
            ('givenname', user['username'].encode("UTF-8")),
            ('sn', user['username'].encode("UTF-8")),
            ('mail', user['email'].encode("UTF-8")),
            ('uidNumber', user['uid'].encode("UTF-8")),
            ('gidNumber', str(gid).encode("UTF-8")),
            ('loginShell', [b'/bin/sh']),
            ('homeDirectory', home_dir.encode("UTF-8")),
            ('userPassword', [b'{md5}' +
                              b64encode(hashed_pwd.digest())])

        ])

        # connect to host with admin
        ldap_conn = ldap.initialize(self.ldap_server)
        ldap_conn.simple_bind_s(self.LDAP_ADMIN_DN, self.LDAP_ADMIN_PWD)

        try:
            search_filter = "cn=" + user['username']
            result = ldap_conn.search_s(LDAP_BASE_DN, ldap.SCOPE_SUBTREE, search_filter)
            # print(result)
            # add entry in the directory
            if not result:
                ldap_conn.add_s(dn, entry)
                return None
            else:
                print("user already exists !!!")
                return "user already exists !!!"
            
        finally:
            # disconnect and free memory
            ldap_conn.unbind_s()



# enter admin password
load_dotenv()
# pwd=os.environ.get('ADMIN_PWD')
# print(pwd)
s = LdapServer(admin_pwd=os.environ['ADMIN_PWD'])
# Test :
# test login
# s.login(username="bo3", password="1234")

# test register
user_toAdd = {
    'username': 'bo3',
    'password': '1234',
    'email': 'bo3@gmail.com',
    'gender': 'male',
    'group_id': 5000,  
    'uid': '11001'  
}
# s.register(user_toAdd)
