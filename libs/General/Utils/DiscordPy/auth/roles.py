

def MemberHasStringInRoles(Member, has='hasTHISONETHING'):
    found=False
    for role in Member.roles:
        # print(f'has "{has}"     EXISTS ?       role.name "{role.name}"')
        if has in str(role.name):
            found=True
    return found

