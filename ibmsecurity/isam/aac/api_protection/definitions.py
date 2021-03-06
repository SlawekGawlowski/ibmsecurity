import logging

logger = logging.getLogger(__name__)

# URI for this module
uri = "/iam/access/v8/definitions"
requires_modules = ["mga"]
requires_version = None


def get_all(isamAppliance, check_mode=False, force=False):
    """
    Retrieve a list of API protection definitions
    """
    return isamAppliance.invoke_get("Retrieve a list of API protection definitions", uri,
                                    requires_modules=requires_modules,
                                    requires_version=requires_version)


def get(isamAppliance, name, check_mode=False, force=False):
    """
    Retrieve a specific API protection definition
    """
    ret_obj = search(isamAppliance, name=name, check_mode=check_mode, force=force)
    defn_id = ret_obj['data']
    warnings = ret_obj["warnings"]

    if defn_id == {}:
        logger.info("Definition {0} had no match, skipping retrieval.".format(name))
        warnings.append("Definition Name {0} had no match.".format(name))
        return isamAppliance.create_return_object(warnings=warnings)
    else:
        return _get(isamAppliance, defn_id)


def _get(isamAppliance, defn_id):
    return isamAppliance.invoke_get("Retrieve a specific API protection definition",
                                    "{0}/{1}".format(uri, defn_id), requires_modules=requires_modules,
                                    requires_version=requires_version)


def search(isamAppliance, name, check_mode=False, force=False):
    """
    Search definition id by name
    """
    ret_obj = get_all(isamAppliance)
    return_obj = isamAppliance.create_return_object()
    return_obj["warnings"] = ret_obj["warnings"]

    for obj in ret_obj['data']:
        if obj['name'] == name:
            logger.info("Found definition {0} id: {1}".format(name, obj['id']))
            return_obj['data'] = obj['id']
            return_obj['rc'] = 0

    return return_obj


def add(isamAppliance, name, description="", grantTypes=["AUTHORIZATION_CODE"], tcmBehavior="NEVER_PROMPT",
        accessTokenLifetime=3600, accessTokenLength=20, enforceSingleUseAuthorizationGrant=False,
        authorizationCodeLifetime=300, authorizationCodeLength=30, issueRefreshToken=True, refreshTokenLength=40,
        maxAuthorizationGrantLifetime=604800, enforceSingleAccessTokenPerGrant=False,
        enableMultipleRefreshTokensForFaultTolerance=False, pinPolicyEnabled=False, pinLength=4,
        tokenCharSet="0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz", check_mode=False, force=False):
    """
    Create an API protection definition
    """
    if (isinstance(grantTypes, basestring)):
        import ast
        grantTypes = ast.literal_eval(grantTypes)

    ret_obj = search(isamAppliance, name=name, check_mode=check_mode, force=force)
    warnings = ret_obj["warnings"]

    if force is True or ret_obj["data"] == {}:
        if check_mode is True:
            return isamAppliance.create_return_object(changed=True, warnings=warnings)
        else:
            return isamAppliance.invoke_post(
                "Create an API protection definition", uri,
                {
                    "name": name,
                    "description": description,
                    "grantTypes": grantTypes,
                    "tcmBehavior": tcmBehavior,
                    "accessTokenLifetime": accessTokenLifetime,
                    "accessTokenLength": accessTokenLength,
                    "enforceSingleUseAuthorizationGrant": enforceSingleUseAuthorizationGrant,
                    "authorizationCodeLifetime": authorizationCodeLifetime,
                    "authorizationCodeLength": authorizationCodeLength,
                    "issueRefreshToken": issueRefreshToken,
                    "refreshTokenLength": refreshTokenLength,
                    "maxAuthorizationGrantLifetime": maxAuthorizationGrantLifetime,
                    "enforceSingleAccessTokenPerGrant": enforceSingleAccessTokenPerGrant,
                    "enableMultipleRefreshTokensForFaultTolerance": enableMultipleRefreshTokensForFaultTolerance,
                    "pinPolicyEnabled": pinPolicyEnabled,
                    "pinLength": pinLength,
                    "tokenCharSet": tokenCharSet
                }, requires_modules=requires_modules, requires_version=requires_version, warnings=warnings)

    return isamAppliance.create_return_object(warnings=warnings)


def delete(isamAppliance, name, check_mode=False, force=False):
    """
    Delete an API protection definition
    """
    ret_obj = search(isamAppliance, name, check_mode=check_mode, force=force)
    defn_id = ret_obj['data']
    warnings = ret_obj["warnings"]

    if defn_id == {}:
        logger.info("Definition {0} not found, skipping delete.".format(name))
    else:
        if check_mode is True:
            return isamAppliance.create_return_object(changed=True, warnings=warnings)
        else:
            return isamAppliance.invoke_delete(
                "Delete an API protection definition",
                "{0}/{1}".format(uri, defn_id), requires_modules=requires_modules,
                requires_version=requires_version, warnings=warnings)

    return isamAppliance.create_return_object(warnings=warnings)


def update(isamAppliance, name, description="", grantTypes=["AUTHORIZATION_CODE"], tcmBehavior="NEVER_PROMPT",
           accessTokenLifetime=3600, accessTokenLength=20, enforceSingleUseAuthorizationGrant=False,
           authorizationCodeLifetime=300, authorizationCodeLength=30, issueRefreshToken=True, refreshTokenLength=40,
           maxAuthorizationGrantLifetime=604800, enforceSingleAccessTokenPerGrant=False,
           enableMultipleRefreshTokensForFaultTolerance=False, pinPolicyEnabled=False, pinLength=4,
           tokenCharSet="0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz", check_mode=False,
           force=False):
    """
    Update a specified API protection definition
    """
    ret_obj = get(isamAppliance, name)
    warnings = ret_obj["warnings"]

    if ret_obj["data"] == {}:
        warnings.append("Definiton {0} not found, skipping update.".format(name))
        return isamAppliance.create_return_object(warnings=warnings)
    else:
        defn_id = ret_obj["data"]["id"]

    needs_update = False
    json_data = {
        "name": name,
        "description": description,
        "grantTypes": grantTypes,
        "tcmBehavior": tcmBehavior,
        "accessTokenLifetime": accessTokenLifetime,
        "accessTokenLength": accessTokenLength,
        "enforceSingleUseAuthorizationGrant": enforceSingleUseAuthorizationGrant,
        "authorizationCodeLifetime": authorizationCodeLifetime,
        "authorizationCodeLength": authorizationCodeLength,
        "issueRefreshToken": issueRefreshToken,
        "refreshTokenLength": refreshTokenLength,
        "maxAuthorizationGrantLifetime": maxAuthorizationGrantLifetime,
        "enforceSingleAccessTokenPerGrant": enforceSingleAccessTokenPerGrant,
        "enableMultipleRefreshTokensForFaultTolerance": enableMultipleRefreshTokensForFaultTolerance,
        "pinPolicyEnabled": pinPolicyEnabled,
        "pinLength": pinLength,
        "tokenCharSet": tokenCharSet
    }

    if force is not True:
        if 'datecreated' in ret_obj['data']:
            del ret_obj['data']['datecreated']
        if 'id' in ret_obj['data']:
            del ret_obj['data']['id']
        if 'lastmodified' in ret_obj['data']:
            del ret_obj['data']['lastmodified']
        if 'mappingRules' in ret_obj['data']:
            del ret_obj['data']['mappingRules']
        import ibmsecurity.utilities.tools
        if ibmsecurity.utilities.tools.json_sort(ret_obj['data']) != ibmsecurity.utilities.tools.json_sort(
                json_data):
            needs_update = True

    if force is True or needs_update is True:
        if check_mode is True:
            return isamAppliance.create_return_object(changed=True, warnings=warnings)
        else:
            return isamAppliance.invoke_put(
                "Update a specified API protection definition",
                "{0}/{1}".format(uri, defn_id), json_data, requires_modules=requires_modules,
                requires_version=requires_version, warnings=warnings)

    return isamAppliance.create_return_object(warnings=warnings)


def set(isamAppliance, name, description="", grantTypes=["AUTHORIZATION_CODE"], tcmBehavior="NEVER_PROMPT",
        accessTokenLifetime=3600, accessTokenLength=20, enforceSingleUseAuthorizationGrant=False,
        authorizationCodeLifetime=300, authorizationCodeLength=30, issueRefreshToken=True, refreshTokenLength=40,
        maxAuthorizationGrantLifetime=604800, enforceSingleAccessTokenPerGrant=False,
        enableMultipleRefreshTokensForFaultTolerance=False, pinPolicyEnabled=False, pinLength=4,
        tokenCharSet="0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz", check_mode=False,
        force=False):
    """
    Creating or Modifying an API Protection Definition
    """
    if (search(isamAppliance, name=name))['data'] == {}:
        # Force the add - we already know policy does not exist
        logger.info("Definition {0} had no match, requesting to add new one.".format(name))
        return add(isamAppliance=isamAppliance, name=name, description=description, grantTypes=grantTypes,
                   tcmBehavior=tcmBehavior,
                   accessTokenLifetime=accessTokenLifetime, accessTokenLength=accessTokenLength,
                   enforceSingleUseAuthorizationGrant=enforceSingleUseAuthorizationGrant,
                   authorizationCodeLifetime=authorizationCodeLifetime, authorizationCodeLength=authorizationCodeLength,
                   issueRefreshToken=issueRefreshToken, refreshTokenLength=refreshTokenLength,
                   maxAuthorizationGrantLifetime=maxAuthorizationGrantLifetime,
                   enforceSingleAccessTokenPerGrant=enforceSingleAccessTokenPerGrant,
                   enableMultipleRefreshTokensForFaultTolerance=enableMultipleRefreshTokensForFaultTolerance,
                   pinPolicyEnabled=pinPolicyEnabled, pinLength=pinLength,
                   tokenCharSet=tokenCharSet, check_mode=check_mode, force=True)
    else:
        # Update request
        logger.info("Definition {0} exists, requesting to update.".format(name))
        return update(isamAppliance=isamAppliance, name=name, description=description, grantTypes=grantTypes,
                      tcmBehavior=tcmBehavior,
                      accessTokenLifetime=accessTokenLifetime, accessTokenLength=accessTokenLength,
                      enforceSingleUseAuthorizationGrant=enforceSingleUseAuthorizationGrant,
                      authorizationCodeLifetime=authorizationCodeLifetime,
                      authorizationCodeLength=authorizationCodeLength, issueRefreshToken=issueRefreshToken,
                      refreshTokenLength=refreshTokenLength,
                      maxAuthorizationGrantLifetime=maxAuthorizationGrantLifetime,
                      enforceSingleAccessTokenPerGrant=enforceSingleAccessTokenPerGrant,
                      enableMultipleRefreshTokensForFaultTolerance=enableMultipleRefreshTokensForFaultTolerance,
                      pinPolicyEnabled=pinPolicyEnabled, pinLength=pinLength,
                      tokenCharSet=tokenCharSet, check_mode=check_mode, force=force)


def compare(isamAppliance1, isamAppliance2):
    """
    Compare API Protection Definitions between two appliances
    """
    ret_obj1 = get_all(isamAppliance1)
    ret_obj2 = get_all(isamAppliance2)

    for obj in ret_obj1['data']:
        del obj['id']
        del obj['datecreated']
        del obj['lastmodified']
        for rules in obj['mappingRules']:
            del rules['id']
    for obj in ret_obj2['data']:
        del obj['id']
        del obj['datecreated']
        del obj['lastmodified']
        for rules in obj['mappingRules']:
            del rules['id']

    import ibmsecurity.utilities.tools
    return ibmsecurity.utilities.tools.json_compare(ret_obj1, ret_obj2,
                                                    deleted_keys=['id', 'datecreated', 'lastmodified',
                                                                  'mappingRules/id'])
