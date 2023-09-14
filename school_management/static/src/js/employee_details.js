/** @odoo-module **/

import publicWidget from 'web.public.widget';

publicWidget.registry.EmployeesDetails = publicWidget.Widget.extend({
    selector: '.employees-details',
    start() {
        let employeesRow = this.el.querySelector('#employees-details-row');

        if (employeesRow) {
            this._rpc({
                route: '/employee/',  
                params: {},           
            }).then(data => {
                let html = '';
                data.forEach(employee => {
                    html += `<div class="col-lg-3 mb-5">
                        <div class="d-flex align-items-center">
                            <div class="img-container mr-3 rounded">
                                <img class="employee-image rounded" src="data:image/png;base64,${employee.emp_image}"/>
                            </div>
                            <div>
                                <h5 class="mb-0">${employee.emp_name || ''}</h5>
                                <div>${employee.emp_phone_number || ''}</div>
                                <div>${employee.emp_work_exp || ''}</div>
                                <div>${employee.emp_city || ''}</div>
                            </div>
                        </div>
                    </div>`;
                });
                employeesRow.innerHTML = html;
            });
        }
    },
});

export default publicWidget.registry.EmployeesDetails;