from core.check import Check
from utils.loggers import log
from utils import rand
import string

class Freemarker(Check):
    
    def init(self):
        
        # Declare payload
        self.base_tag = '${%s}'
        
        self.req_header_rand = str(rand.randint_n(4))
        self.req_trailer_rand = str(rand.randint_n(4))
        
        # Skip reflection check if same tag has been detected before
        if self.get('reflect_tag') != self.base_tag:
            self._check_reflection()
        
            # Return if reflect_tag is not set
            if not self.get('reflect_tag'):
                return
                
            log.warn('Reflection detected with tag \'%s\'' % self.get('reflect_tag'))
    
    def req(self, payload):
    
        # Rewrite req to include Freemarker number formatting
        # 3333 -> 3,333
        
        req_header = self.base_tag % self.req_header_rand
        req_trailer = self.base_tag % self.req_trailer_rand
        
        req_header_rand_formatted = self.req_header_rand[:1] + ',' + self.req_header_rand[1:]
        req_trailer_rand_formatted = self.req_trailer_rand[:1] + ',' + self.req_trailer_rand[1:]

        response = self.channel.req(req_header + payload + req_trailer)
        before,_,result = response.partition(req_header_rand_formatted)
        result,_,after = result.partition(req_trailer_rand_formatted)
        
        return result.strip()