hqDefine("scheduling/js/conditional_alert_list", function() {
    var table = null;

    $(function() {
        var conditonal_alert_list_url = hqImport("hqwebapp/js/initial_page_data").reverse("conditional_alert_list");

        table = $("#conditional-alert-list").dataTable({
            "lengthChange": false,
            "filter": false,
            "sort": false,
            "displayLength": 10,
            "processing": false,
            "serverSide": true,
            "ajaxSource": conditonal_alert_list_url,
            "fnServerParams": function(aoData) {
                aoData.push({"name": "action", "value": "list_conditional_alerts"});
            },
            "sDom": "rtp",
            "language": {
                "emptyTable": gettext('There are no alerts to display.'),
                "infoEmpty": gettext('There are no alerts to display.'),
                "info": gettext('Showing _START_ to _END_ of _TOTAL_ alerts'),
            },
            "columns": [
                {"data": ""},
                {"data": "name"},
                {"data": "case_type"},
                {"data": "active"},
                {"data": ""},
            ],
            "columnDefs": [
                {
                    "targets": [0],
                    "className": "text-center",
                    "render": function(data, type, row) {
                        var button_id = 'delete-button-for-' + row.id;
                        var disabled = row.locked_for_editing ? 'disabled' : '';
                        return '<button id="' + button_id + '" \
                                        class="btn btn-danger" \
                                        onclick="hqImport(\'scheduling/js/conditional_alert_list\').deleteAlert(' + row.id + ')" \
                                        ' + disabled + '> \
                                <i class="fa fa-remove"></i></button>';
                    },
                },
                {
                    "targets": [1],
                    "render": function(data, type, row) {
                        var url = hqImport("hqwebapp/js/initial_page_data").reverse('edit_conditional_alert', row.id);
                        return "<a href='" + url + "'>" + row.name + "</a>";
                    },
                },
                {
                    "targets": [3],
                    "render": function(data, type, row) {
                        var active_text = '';
                        if(row.active) {
                            active_text = '<span class="label label-success">' + gettext("Active") + '</span> ';
                        } else {
                            active_text = '<span class="label label-danger">' + gettext("Inactive") + '</span> ';
                        }

                        var processing_text = '';
                        if(row.locked_for_editing) {
                            processing_text = '<span class="label label-default">' + gettext("Rule is processing") + ': ' + row.progress_pct + '%</span> ';
                        }

                        return active_text + processing_text;
                    },
                },
                {
                    "targets": [4],
                    "render": function(data, type, row) {
                        var html = null;
                        var button_id = 'activate-button-for-' + row.id;
                        var disabled = (row.locked_for_editing || !row.editable) ? 'disabled' : '';
                        if(row.active) {
                            html = '<button id="' + button_id + '" \
                                            class="btn btn-default" \
                                            onclick="hqImport(\'scheduling/js/conditional_alert_list\').deactivateAlert(' + row.id + ')" \
                                            ' + disabled + '> \
                                   ' + gettext("Deactivate") + '</button>';
                        } else {
                            html = '<button id="' + button_id + '" + \
                                            class="btn btn-default" + \
                                            onclick="hqImport(\'scheduling/js/conditional_alert_list\').activateAlert(' + row.id + ')" \
                                            ' + disabled + '> \
                                   ' + gettext("Activate") + '</button>';
                        }

                        if(row.locked_for_editing) {
                            html += ' <button class="btn btn-default" onclick="hqImport(\'scheduling/js/conditional_alert_list\').restartRule(' + row.id + ')">';
                            html += '<i class="fa fa-refresh"></i> ' + gettext("Restart Rule") + '</button>';
                        }

                        return html;
                    },
                },
            ],
        });

        function reloadTable() {
            table.fnDraw(false);
            setTimeout(reloadTable, 10000);
        }

        setTimeout(reloadTable, 10000);

    });

    function alertAction(action, rule_id) {
        var activateButton = $('#activate-button-for-' + rule_id);
        var deleteButton = $('#delete-button-for-' + rule_id);
        if(action === 'delete') {
            deleteButton.disableButton();
            activateButton.prop('disabled', true);
        } else if (action === 'activate' || action === 'deactivate') {
            activateButton.disableButton();
            deleteButton.prop('disabled', true);
        }

        $.ajax({
            url: '',
            type: 'post',
            dataType: 'json',
            data: {
                action: action,
                rule_id: rule_id,
            },
        })
            .done(function(result) {
                if(action === 'restart') {
                    if(result.status === 'success') {
                        alert(gettext("This rule has been restarted."));
                    } else if(result.status === 'error') {
                        var text = gettext(
                            "Unable to restart rule. Rules can only be started every two hours and there are " +
                            "%s minute(s) remaining before this rule can be started again."
                        );
                        text = interpolate(text, [result.minutes_remaining]);
                        alert(text);
                    }
                }
            })
            .always(function() {
                table.fnDraw(false);
            });
    }

    function activateAlert(rule_id) {
        alertAction('activate', rule_id);
    }

    function deactivateAlert(rule_id) {
        alertAction('deactivate', rule_id);
    }

    function deleteAlert(rule_id) {
        if(confirm(gettext("Are you sure you want to delete this conditional message?"))) {
            alertAction('delete', rule_id);
        }
    }

    function restartRule(rule_id) {
        var prompt = null;
        if(hqImport("hqwebapp/js/initial_page_data").get("limit_rule_restarts")) {
            prompt = gettext(
                "A rule should only be restarted when you believe it is stuck and is not progressing. " +
                "You will only be able to restart this rule once every two hours. Restart this rule?"
            );
        } else {
            prompt = gettext(
                "A rule should only be restarted when you believe it is stuck and is not progressing. " +
                "Your user is able to restart as many times as you like, but restarting too many times without " +
                "finishing can place a burden on the system. Restart this rule?"
            );
        }
        if(confirm(prompt)) {
            alertAction('restart', rule_id);
        }
    }

    return {
        activateAlert: activateAlert,
        deactivateAlert: deactivateAlert,
        deleteAlert: deleteAlert,
        restartRule: restartRule,
    };
});
