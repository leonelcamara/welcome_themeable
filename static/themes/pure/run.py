class MENU(DIV):
    """
    Used to build menus

    Args:
        _class: defaults to 'web2py-menu web2py-menu-vertical'
        ul_class: defaults to 'web2py-menu-vertical'
        li_class: defaults to 'web2py-menu-expand'
        li_first: defaults to 'web2py-menu-first'
        li_last: defaults to 'web2py-menu-last'

    Use like::

        menu = MENU([['name', False, URL(...), [submenu]], ...])
        {{=menu}}

    """

    tag = 'ul'

    def __init__(self, data, **args):
        self.data = data
        self.attributes = args
        self.components = []
        if not '_class' in self.attributes:
            self['_class'] = 'web2py-menu web2py-menu-vertical'
        if not 'ul_class' in self.attributes:
            self['ul_class'] = 'web2py-menu-vertical'
        if not 'li_class' in self.attributes:
            self['li_class'] = 'web2py-menu-expand'
        if not 'li_first' in self.attributes:
            self['li_first'] = 'web2py-menu-first'
        if not 'li_last' in self.attributes:
            self['li_last'] = 'web2py-menu-last'
        if not 'li_active' in self.attributes:
            self['li_active'] = 'web2py-menu-active'
        if not 'mobile' in self.attributes:
            self['mobile'] = False

    def serialize(self, data, level=0):
        if level == 0:
            ul = UL(**self.attributes)
        else:
            ul = UL(_class=self['ul_class'])
        for item in data:
            if isinstance(item, LI):
                ul.append(item)
            else:
                (name, active, link) = item[:3]
                if isinstance(link, DIV):
                    li = LI(link)
                elif 'no_link_url' in self.attributes and self['no_link_url'] == link:
                    li = LI(DIV(name))
                elif isinstance(link, dict):
                    li = LI(A(name, **link))
                elif link:
                    li = LI(A(name, _href=link, _class='pure-menu-link'))
                elif not link and isinstance(name, A):
                    link['_class']='pure-menu-link'
                    li = LI(name)
                else:
                    li = LI(A(name, _href='#',
                              _onclick='javascript:void(0);return false;', _class='pure-menu-link'))
                li['_class'] = 'pure-menu-item'
                if level == 0 and item == data[0]:
                    li['_class'] += ' ' + self['li_first']
                elif level == 0 and item == data[-1]:
                    li['_class'] += ' ' + self['li_last']
                if len(item) > 3 and item[3]:
                    li['_class'] += ' ' + self['li_class']
                    li.append(self.serialize(item[3], level + 1))
                if active or ('active_url' in self.attributes and self['active_url'] == link):
                    li['_class'] = li['_class'] + ' ' + self['li_active']
                if len(item) <= 4 or item[4] == True:
                    ul.append(li)
        return ul

    def xml(self):
        return self.serialize(self.data, 0).xml()


def purenavbar(auth_navbar):
    bar = auth_navbar
    user = bar['user']
    children = UL(_class='pure-menu-children')
    li = LI(A(T('Log In') if not user else '%s %s' % (bar["prefix"], user), _href='#', _onclick='javascript:void(0);return false;', _class='pure-menu-link'), children, _class='pure-menu-item pure-menu-has-children pure-menu-allow-hover')

    if not user:
        children.append(LI(A(T('Sign Up'), _href=bar['register'], _class='pure-menu-link'), _class='pure-menu-item'))
        children.append(LI(A(T('Lost password?'), _href=bar['request_reset_password'], _class='pure-menu-link'), _class='pure-menu-item'))
        children.append(LI(A(T('Log In'), _href=bar['login'], _class='pure-menu-link'), _class='pure-menu-item'))
    else:
        children.append(LI(A(T('Profile'), _href=bar['profile'], _class='pure-menu-link'), _class='pure-menu-item'))
        children.append(LI(A(T('Password'), _href=bar['change_password'], _class='pure-menu-link'), _class='pure-menu-item'))
        children.append(LI(A(T('Log Out'), _href=bar['logout'], _class='pure-menu-link'), _class='pure-menu-item'))

    return li


def formstyle_pure_aligned(form, fields):
    form.add_class('pure-form pure-form-aligned')

    def add_button(self, value, url, _class=None):
        submit = self.element(_type='submit')
        _class = "%s pure-button w2p-form-button" % _class if _class else "pure-button w2p-form-button"
        submit.parent.append(
            TAG['button'](value, _class=_class,
                          _onclick=url if url.startswith('javascript:') else
                          self.REDIRECT_JS % url))
    
    import types
    form.add_button = types.MethodType(add_button, form)

    parent = FIELDSET()
    for id, label, controls, help in fields:
        # wrappers
        _help = SPAN(help, _class='help-inline')
        # submit unflag by default
        _submit = False
        _checkbox = False

        if isinstance(controls, INPUT):
            controls.add_class('span4')
            if controls['_type'] == 'submit':
                # flag submit button
                _submit = True
                controls['_class'] = 'pure-button pure-button-primary'
            elif controls['_type'] == 'checkbox':
                _checkbox = True
                label['_class'] = 'pure-checkbox'

        if _submit:
            # submit button has unwrapped label and controls, different class
            parent.append(DIV(label, controls, _class='pure-controls'))
        elif _checkbox:
            label.append(controls)
            parent.append(DIV(label, _help, _class='pure-controls'))
        else:
            # unwrapped label
            parent.append(DIV(label, controls, _help, _class='pure-control-group', _id=id))
    return parent

response.formstyle = formstyle_pure_aligned
auth.settings.formstyle = formstyle_pure_aligned