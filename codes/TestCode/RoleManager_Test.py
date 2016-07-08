
from RoleModule.role_manager import RoleManager

roleMgr = RoleManager()

roleMgr.create_role(roleType = "PlayerRole",
                    name = "playerrole1",
                    actions = {
                        "action1" : "walk",
                        "action2" : "run"
                    },
                    modelId = "actor1")

roleMgr.create_role(roleType= "EnemyRole",
                    name = "Zombie",
                    actions = {
                        "action1": "walk",
                        "action2": "run"
                    },
                    modelId = "Zombie",
                    num = 10)

roleMgr.print_roleModelMap()
roleMgr.print_roleNameMap()

role = roleMgr.get_role("playerrole1")
role.print_all_attr()