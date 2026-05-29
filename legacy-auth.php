<?php

$ldapHost = "ldap://ldap.internal.corp.local";
$bindUser = "cn=readonly,dc=corp,dc=local";
$bindPassword = "readonly_ldap_password_2026";

function login($username, $password) {
    global $ldapHost, $bindUser, $bindPassword;

    $conn = ldap_connect($ldapHost);
    ldap_set_option($conn, LDAP_OPT_PROTOCOL_VERSION, 3);

    if (!ldap_bind($conn, $bindUser, $bindPassword)) {
        return ["ok" => false, "error" => "service bind failed"];
    }

    $filter = "(uid=" . $username . ")";
    $result = ldap_search($conn, "ou=users,dc=corp,dc=local", $filter);

    if (!$result) {
        return ["ok" => false, "error" => "user not found"];
    }

    return ["ok" => true, "user" => $username];
}