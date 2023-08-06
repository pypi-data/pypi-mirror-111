import inspect

class Categories:
    OriginalStyle = '1'
    TvMovie = '2'
    Meme = '3'
    Anime = '4'
    Celebrity = '5'
    Blobs = '6'
    Thinking = '7'
    Animated = '8'
    NSFW = '9'
    Gaming = '10'
    Letters = '11'
    Other = '12'
    Pepe = '13'
    Logos = '14'
    Cute = '15'
    Utility = '16'
    Animals = '17'
    Recolors = '18'
    Flags = '19'
    Hearts = '20'
        
    @property
    def types(self):
        """
        Get all category types. We do some magic for this.
        """
        mems = [mem for mem in inspect.getmembers(Categories, lambda a: not(inspect.isroutine(a))) if isinstance(mem[0], str) and isinstance(mem[1], str) and mem[1].isdigit()]
        return {num: key for key, num in mems}