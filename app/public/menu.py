

menu_top = [
    {
        "label": "首页",
        "path": "/dashboard",
        "icon": 'el-icon-s-home',
        "meta": {
            "i18n": 'dashboard',
        },
        "parentId": 0
    }
]

first = [
    {
        "label": "用户",
        "path": '/user',
        "meta": {
            "i18n": 'user',
        },
        "icon": 'el-icon-setting',
        "children": [
            {
                "label": "用户列表",
                "path": 'user',
                "component": 'views/custom/user/user',
                "meta": {
                    "i18n": 'user'
                },
                "icon": 'el-icon-setting',
                "children": []
            },
        ]
    },
    {
        "label": "公共",
        "path": '/publicinfo',
        "meta": {
            "i18n": 'publicinfo',
        },
        "icon": 'el-icon-setting',
        "children": [
            {
                "label": "轮播图",
                "path": 'banner',
                "component": 'views/custom/publicinfo/banner',
                "meta": {
                    "i18n": 'banner'
                },
                "icon": 'el-icon-setting',
                "children": []
            },
            {
                "label": "节假日维护",
                "path": 'holiday',
                "component": 'views/custom/publicinfo/holiday',
                "meta": {
                    "i18n": 'holiday'
                },
                "icon": 'el-icon-setting',
                "children": []
            }
        ]
    },
    {
        "label": "彩票",
        "path": '/cpinfo',
        "meta": {
            "i18n": 'cpinfo',
        },
        "icon": 'el-icon-setting',
        "children": [
            {
                "label": "彩票类型",
                "path": 'cpTypes',
                "meta": {
                    "i18n": 'cpTypes',
                },
                "icon": 'el-icon-setting',
                "children":[
                    {
                        "label": "彩票大类",
                        "path": 'cpbigtype',
                        "component": 'views/custom/cpinfo/cpTypes/cpbigtype',
                        "meta": {
                            "i18n": 'cpbigtype'
                        },
                        "icon": 'el-icon-setting',
                        "children": []
                    },
                    {
                        "label": "彩票中类",
                        "path": 'cpsmalltype',
                        "component": 'views/custom/cpinfo/cpTypes/cpsmalltype',
                        "meta": {
                            "i18n": 'cpsmalltype'
                        },
                        "icon": 'el-icon-setting',
                        "children": []
                    },
                    {
                        "label": "彩票小类",
                        "path": 'cpminitype',
                        "component": 'views/custom/cpinfo/cpTypes/cpminitype',
                        "meta": {
                            "i18n": 'cpminitype'
                        },
                        "icon": 'el-icon-setting',
                        "children": []
                    },
                    {
                        "label": "彩票玩法",
                        "path": 'cpgames',
                        "component": 'views/custom/cpinfo/cpTypes/cpgames',
                        "meta": {
                            "i18n": 'cpgames'
                        },
                        "icon": 'el-icon-setting',
                        "children": []
                    },
                ]
            },
            {
                "label": "彩票",
                "path": 'cp',
                "component": 'views/custom/cpinfo/cp',
                "meta": {
                    "i18n": 'cp'
                },
                "icon": 'el-icon-setting',
                "children": []
            }
        ]
    },
    {
        "label": "订单管理",
        "path": '/orderinfo',
        "meta": {
            "i18n": 'orderinfo',
        },
        "icon": 'el-icon-setting',
        "children": [
            {
                "label": "订单列表",
                "path": 'order',
                "component": 'views/custom/orderinfo/order',
                "meta": {
                    "i18n": 'order'
                },
                "icon": 'el-icon-setting',
                "children": []
            }
        ]
    },
    {
        "label": "系统管理",
        "path": '/systemManagement',
        "meta": {
            "i18n": 'systemManagement',
        },
        "icon": 'el-icon-setting',
        "children": [
            {
                "label": "系统设置",
                "path": 'sys_setting',
                "component": 'views/custom/systeminfo/sys_setting',
                "meta": {
                    "i18n": 'sys_setting'
                },
                "icon": 'el-icon-setting',
                "children": []
            },
            {
                "label": "app版本管理",
                "path": 'appHandler',
                "component": 'views/custom/systeminfo/appHandler',
                "meta": {
                    "i18n": 'appHandler'
                },
                "icon": 'el-icon-setting',
                "children": []
            },
            {
                "label": "初始化项目",
                "path": 'InitProject',
                "component": 'views/custom/systeminfo/InitProject',
                "meta": {
                    "i18n": 'InitProject'
                },
                "icon": 'el-icon-setting',
                "children": []
            },
            {
                "label": "刷新缓存",
                "path": 'Cache',
                "component": 'views/custom/systeminfo/Cache',
                "meta": {
                    "i18n": 'Cache'
                },
                "icon": 'el-icon-setting',
                "children": []
            }
        ]
    }
]


all_menu = {
    "top" : menu_top,
    "first" : first
}
