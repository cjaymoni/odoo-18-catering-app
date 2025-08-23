odoo.define("catering_management.dashboard", function (require) {
  "use strict";

  var AbstractAction = require("web.AbstractAction");
  var core = require("web.core");

  var CateringDashboard = AbstractAction.extend({
    template: "CateringDashboard",

    init: function (parent, action) {
      this._super(parent, action);
      this.dashboard_data = {};
    },

    start: function () {
      var self = this;
      return this._super().then(function () {
        return self.load_dashboard_data();
      });
    },

    load_dashboard_data: function () {
      var self = this;
      return this._rpc({
        model: "cater.event.booking",
        method: "get_dashboard_data",
      }).then(function (data) {
        self.dashboard_data = data;
        self.render_dashboard();
      });
    },

    render_dashboard: function () {
      var $content = $(this.template(this.dashboard_data));
      this.$el.html($content);
    },
  });

  core.action_registry.add("catering_dashboard", CateringDashboard);

  return CateringDashboard;
});
