from reports.models import Report
from utils.mixins import QuickReportMixin, ReportUpdateQuickViewMixin, ReportUpdateReporterMixin


class ReportQuickCreateViewV2(QuickReportMixin):
    model = Report
    menu_name = 'report'
    template_name = 'reports/report_quick_form-v2.html'
    permission_required = 'reports.add_report'



class ReportUpdateViewV2(ReportUpdateQuickViewMixin):
    redirect_url = "report-quick-create-v2"
    app_name = "QUICK REPORT V2"
    


class ReportUpdatePetugasView(ReportUpdateReporterMixin):
    redirect_url = "report-quick-create-v2"