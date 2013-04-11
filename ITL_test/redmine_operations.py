from redmine import Redmine

demo = Redmine('http://track.itland.net.ua', username='jenko', password='zcegthuv33')
project = demo.projects['app-server']
#for issue in project.issues:
#    print unicode(issue)
project.issues.new