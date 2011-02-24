function(doc) {
    // these lines magically import our other javascript files.  DON'T REMOVE THEM!
    // !code util/shared_funcs.js

    if (doc.base_type == 'AuditEvent') {
        //by username, and the events they do
        var event_date = parse_date(doc.event_date);
        //user event dates, emit to the class
        emit(['user_date', doc.user, event_date.getFullYear(), event_date.getMonth() +1, event_date.getDate(), event_date.getHours(), event_date.getMinutes(), event_date.getSeconds()], doc.event_class);
    }
}