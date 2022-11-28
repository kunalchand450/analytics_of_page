import json
import os
import tempfile 
import scrapy
import pandas
from json.decoder import JSONDecodeError
class MultiSpider(scrapy.Spider):
    name = "multi_scrapper"
    start_urls = ["http://www.adara.com", "https://stagum.com/", "http://www.anacostiatrails.org", "http://www.aqua.org", "http://www.baltimore.org", "http://www.baltimorecountymd.gov", "http://www.beachesbayswaterways.org", "http://www.berlinmd.gov", "http://www.bluum.com", "http://www.bwbwi.com", "http://www.calvertcountymd.gov", "http://www.carrollbiz.org", "http://www.carrollcountymd.gov", "http://www.celticrnr.com", "http://www.chesapeakebaymagazine.com", "http://www.co.pg.md.us", "http://www.co.worcester.md.us", "http://www.danikapr.com", "http://www.delmarvadiscoverycenter.org", "http://www.docogonet.com", "http://www.e.hps.com", "http://www.enradius.com", "http://www.expediagroup.com", "http://www.flyingdog.com", "http://www.fogo.com", "http://www.harfordbrewtours.com", "http://www.havredegracemd.com", "http://www.higreenbelt.com", "http://www.iheartmedia.com", "http://www.jammintogether.com", "http://www.jmoreliving.com", "http://www.kbssportsstrategies.com", "http://www.kentgov.org", "http://www.kentnarrowsmd.com", "http://www.marriott.com", "http://www.maryland.com", "http://www.marylandmotorcoach.org", "http://www.marylandports.com", "http://www.marylandracing.com", "http://www.marylandroadtrips.com", "http://www.marylandsports.us", "http://www.mcdonnellmedia.com", "http://www.mdsoccerplex.org", "http://www.mediaone.digital", "http://www.mediaonena.com", "http://www.medievaltimes.com", "http://www.missshirleys.com", "http://www.ncm.com", "http://www.ocbeachresort.com", "http://www.oceancity.com", "http://www.oceancity.org", "http://www.ocvisitor.com", "http://www.onpointsportsstrategies.com", "http://www.optonline.net", "http://www.orange.com", "http://www.palmergosnell.com", "http://www.phillipsfoods.com", "http://www.platinumpr.com", "http://www.pressboxonline.com", "http://www.princessbayside.com", "http://www.princessroyale.com", "http://www.recreationnews.com", "http://www.rentatour.com", "http://www.rhgcorp.com", "http://www.salisbury.edu", "http://www.seifertassociatesinc.com", "http://www.smcmail.com", "http://www.sojern.com", "http://www.sonesta.com", "http://www.stratosphere.social.com", "http://www.tccsmd.org", "http://www.tdsbrochure.com", "http://www.todaymediacustom.com", "http://www.trade.gov", "http://www.travelspike.com", "http://www.usna.edu", "http://www.visithagerstown.com", "http://www.visitmaryland.org", "http://www.visitstmarysmd.com", "http://www.wandermaps.com", "http://www.whong.media", "http://www.wispresort.com", "http://www.zartico.com"]
    # start_urls = ["http://www.google.com"]
    def parse(self, response):
        tag_to_analytics_map = {
                "google-analytics": "googleanalytics",
                "googletagmanager": "googletag",
                "adobedtm":"adobedtm",
                "kissmetrics": "kissmetrics",
                }
        response_body = str(response.body)

        try:
        # if True:
            with open('tmp_output.json') as read_obj:
               result_json = json.load(read_obj)
        except (FileNotFoundError, JSONDecodeError) as e:
            print(f'found exception {e} while loading temp output json using empty default')
            result_json = {"url":{},
                           "google-analytics" : {},
                           "googletagmanager" : {},
                           "adobedtm" : {},
                           "kissmetrics": {},
                           }

        # print(vars(response))
        if response.body:
            # print(vars(response))
            result_json['url'][len(result_json['url'].keys()) + 1] = response.url
            for tag in tag_to_analytics_map:
                if tag in response_body:
                    result_json[tag][len(result_json['url'].keys())] = True
                    print(f'{response.url} {tag}: True')
                else:
                    result_json[tag][len(result_json['url'].keys())] = False
                    print(f'{response.url} {tag}: False')
        # if os.path.exists(os.path.join(tempfile.gettempdir(),'tmp_output')):
        #         os.remove(os.path.join(tempfile.gettempdir(),'tmp_output'))            
        with open('tmp_output.json', 'w') as write_obj:
            json.dump(result_json, write_obj)
        pandas.DataFrame.from_dict(result_json).to_csv('website_tags.csv', encoding='utf-8', index=False)
