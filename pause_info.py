from termcolor import colored


class PauseInfo:
    """
    Class that shows summaries on pauses from a given log.
    """

    def __init__(self, mixed_parser):
        """
        Defines the needed times pauses for the PauseInfo class.
        """
        self._mixed_parser = mixed_parser

    def _is_short_pause(self, pause):
        """
        Determines if a pause is a short one.
        - pause is in milliseconds
        - a short pause is between 2 and 6 seconds
        """
        return 2000 <= pause and pause < 6000

    def _is_medium_pause(self, pause):
        """
        Determines if a pause is a medium one.
        - pause is in milliseconds
        - a medium pause is between 6 and 60 seconds
        """
        return 6000 <= pause and pause < 60000

    def _is_big_pause(self, pause):
        """
        Determines if a pause is a big one.
        - pause is in milliseconds
        - a big pause is greater than 60 seconds
        """
        return pause >= 60000

    def get_pauses(self, begin, end):
        """
        Given an interval in which pauses should be look for.
        It returns the duration of the pauses and the millisecond in which they
        started.
        """
        pauses = []
        for i in range(len(self._mixed_parser.keys) - 1):
            # Get current keystroke.
            cdate, ctime, cprogram_name, cusername, cwindow_id, cwindow_title, cmiliseconds, ckey, cmsg, cxcoord, cycoord = self._mixed_parser.keys[
                i]
            # Get next keystroke.
            ndate, ntime, nprogram_name, nusername, nwindow_id, nwindow_title, nmiliseconds, nkey, nmsg, nxcoord, nycoord = self._mixed_parser.keys[
                i + 1]
            if begin <= min(int(nmiliseconds), int(cmiliseconds)) and max(int(nmiliseconds), int(cmiliseconds)) <= end:
                pauses += [(int(cmiliseconds),
                            int(nmiliseconds) - int(cmiliseconds))]
        return pauses

    def print_pauses(self, begin, end):
        """
        Prints a summary of the short, medium and big pauses in the session.
        All pauses that do not fall in these categories are ignored.
        """
        pauses = self.get_pauses(begin, end)
        i = 0
        for pause in pauses:
            i += 1
            if self._is_short_pause(pause):
                print "Pausa #", i, ":", colored(str(pause), "green"), "ms"
            elif self._is_medium_pause(pause):
                print "Pausa #", i, ":", colored(str(pause), "yellow"), "ms"
            elif self._is_big_pause(pause):
                # It's a big pause
                print "Pausa #", i, ":", colored(str(pause), "red"), "ms"

    def print_pause_summary(self, begin, end):
        pauses = self.get_pauses(begin, end)
        # Set how many pauses occurred and which types.
        short_pauses, medium_pauses, big_pauses = 0, 0, 0
        sum_pauses = 0
        var_pauses = 0
        for pause in pauses:
            start, duration = pause
            sum_pauses += duration
            var_pauses += duration * duration
            short_pauses += self._is_short_pause(duration)
            medium_pauses += self._is_medium_pause(duration)
            big_pauses += self._is_big_pause(duration)
        # Calculates the variance.
        esp_pauses = sum_pauses / float(len(pauses))
        var_pauses = (1 / float(len(pauses)) * var_pauses) - \
            (esp_pauses * esp_pauses)
        other_pauses = len(pauses) - short_pauses - medium_pauses - big_pauses
        # Print results.
        print "*** RESUMEN DE PAUSAS ***"
        print "Cantidad total de pausas en el intervalo [", begin, "ms ,", end, "ms ]:", colored(len(pauses), "blue")
        print "Cantidad de pausas cortas:", colored(short_pauses, "blue"), "-", colored(short_pauses / float(len(pauses)), "cyan"), "%"
        print "Cantidad de pausas medianas:", colored(medium_pauses, "blue"), "-", colored(medium_pauses / float(len(pauses)), "cyan"), "%"
        print "Cantidad de pausas largas:", colored(big_pauses, "blue"), "-", colored(big_pauses / float(len(pauses)), "cyan"), "%"
        print "Cantidad de pausas no significativas:", colored(other_pauses, "blue"), "-", colored(other_pauses / float(len(pauses)), "cyan"), "%"
        print "Tiempo de pausa promedio:", colored(esp_pauses, "blue")
        print "Varianza en el tiempo de las pausas:", colored(var_pauses, "blue")
