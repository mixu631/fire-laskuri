from jinja2 import Environment, FileSystemLoader
#from weasyprint import HTML
import os

class ReportGenerator:
    def __init__(self, wealth_data, targets, chart_file='wealth_chart.png'):
        """
        Initializes the report generator.

        Args:
            wealth_data (list of dict): Simulation results.
            targets (dict): Dictionary of target milestones.
            chart_file (str): Path to the chart image.
        """
        self.wealth_data = wealth_data
        self.targets = targets
        self.chart_file = chart_file

    def generate_html(self, output_html='report.html'):
        """
        Generates an HTML report.

        Args:
            output_html (str): Filename for the HTML output.
        """
        env = Environment(loader=FileSystemLoader(searchpath='./reports'))
        template = env.get_template('template.html')

        html_out = template.render(
            wealth_data=self.wealth_data,
            targets=self.targets,
            chart_file=self.chart_file
        )

        with open(output_html, 'w', encoding='utf-8') as f:
            f.write(html_out)

        print(f"✅ HTML report saved as {output_html}")

#    def generate_pdf(self, output_pdf='report.pdf'):
#        """
#        Converts the HTML report to PDF.
#
#        Args:
#            output_pdf (str): Filename for the PDF output.
#        """
#        self.generate_html()  # First make sure HTML exists
#        HTML('report.html').write_pdf(output_pdf)
#        print(f"✅ PDF report saved as {output_pdf}")
