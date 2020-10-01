

def get_or_create(session, model, **kwargs):
    instance = session.query(model).filter_by(**kwargs).first()
    
    if not instance:
        instance = model(**kwargs)
        session.add(instance)
        session.commit()
    
    return instance


def get_or_create_and_maybe_update(session, model, keys, values):
    instance = get_or_create(session, model, **keys)
    
    update = False
    for column, new_value in values.items():
        current_value = getattr(instance, column)
        
        if current_value != new_value:
            update = True
            setattr(instance, column, new_value)
    
    if update:
        session.commit()
    
    return instance