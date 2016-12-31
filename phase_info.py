from termcolor import colored


class PhaseInfo:
    """
    Given a corpus with # as the marker for the end of drafting phases.
    This class determines info about the translation phases.
    """

    def __init__(self, mp, slog_filename):
        """
        Initializes the PhaseInfo class with the mixed parser and the system log path.
        """
        self.mixed_parser = copy.copy(mp)
        self.slog_filename = slog_filename
        self._set_phases()

    def _set_phases(self):
        """
        Sets the needed values to calculate the translation phases.
        """
        # Get parser.
        self.clicks = self.mixed_parser.clicks
        self.keys = self.mixed_parser.keys
        # tsparser = mixed_parser.Parser(dfile, cfile, TS)
        # keys = copy.copy(tsparser.keys)
        # Get Clicks.
        self.openClicks = []
        for click in self.clicks:
            if 'Abrir' in click:
                self.openClicks += [click]

        # Planning (Start)
        self.ostime = int(self.openClicks[-1][6])

        # Drafting (End)
        self.detime = 0
        try:
            for k in self.keys:
                match = re.findall(r'[\S]*#', " " + ",".join(k))
                if match != []:
                    self.detime = int(match[0].split(",")[1])
                    break
        except:
            pass

        # Revision (End)
        # try:
        system = open(self.slog_filename, 'r').read()
        self.rostime = re.findall(
            r'[\S]* [\S]* [\S]* [\S]*       [\S]*      [\S]*    [\S]*    [\S]* [\S]* [\S]* [\S]*\n[\S]* [\S]* [\S]*\n[\S]* [\S]* [\S]* [\S]*\n[\S]* [\S]* [\S]*\n[\S]* [\S]*\n[\S]* [\S]*%s' % self.ostime, system)[0].split(",")[0]
        self.rretime = re.findall(r'END: [\S]*', system)[0].split(" ")[1]
        self.rostime = datetime.datetime.strptime(self.rostime, "%H:%M:%S")
        self.rretime = datetime.datetime.strptime(self.rretime, "%H%M%S")
        self.ttime = self.rretime - self.rostime
        self.ttime = str(self.ttime).split(":")
        self.ftime = self.ostime + \
            (int(self.ttime[1]) * 60 + int(self.ttime[2])) * 1000
        self.ttime = (int(self.ttime[1]) * 60 + int(self.ttime[2])) * 1000
        self.retime = self.ftime - self.detime
        self.retime = self.ftime
        self.rstime = self.detime
        self.rtime = self.retime - self.rstime
        # Greatest time seen
        self.greatest_time = self.retime

        # Planning (End)
        self.oetime = int(self.keys[0][6])
        self.otime = self.oetime - self.ostime

        # Drafting (Start)
        self.dstime = self.oetime

        # Revision (Start)
        self.rstime = self.detime
        # Drafting (Show Results)
        self.dtime = self.detime - self.dstime

    def print_orientation_info(self):
        """
        Prints the info on the Planning phase.
        """
        print "*** ORIENTACIÓN ***"
        print "Tiempo de inicio:", colored(self.ostime, 'cyan')
        print "Tiempo de finalización:", colored(self.oetime, 'cyan')
        print "Duración:", colored(self.otime, 'cyan'), "ms =",
        print colored(self.otime / float(1000), 'cyan'), "sec,"
        try:
            print "Porcentaje de la sesión dedicado a la fase de orientación:",
            print colored((self.otime / float(self.ttime)) * 100, 'cyan'), "%"
        except NameError:
            # st - session time
            self.st = max(int(self.keys[-1][6]), int(self.openClicks[-1][6]))
            self.st -= int(self.openClicks[-2][6])
            print "Porcentaje de la sesión dedicado a la fase de orientación:",
            print colored((self.otime / float(self.st)) * 100, 'cyan'), "%"

    def print_drafting_info(self):
        """
        Prints the info on the Drafting phase.
        """
        print "*** ELABORACIÓN DE BORRADOR ***"
        print "Tiempo de inicio:", colored(self.dstime, "cyan")
        print "Tiempo de finalización:", colored(self.detime, "cyan")
        print "Duración:", colored(self.dtime, "cyan"), "ms,",
        print colored(self.dtime / float(1000), "cyan"), "sec,"
        try:
            print "Porcentaje de la sesión dedicado a la fase de elaboración",
            print "de borrador:",
            print colored((self.dtime / float(self.ttime)) * 100, 'cyan'), "%"
        except NameError:
            self.st = max(int(self.keys[-1][6]), int(self.openClicks[-1][6]))
            self.st -= int(self.openClicks[-2][6])
            print "Porcentaje de la sesión dedicado a la fase de elaboración",
            print "de borrador:",
            print colored((self.dtime / float(self.stime)) * 100, "cyan"), "%"

    def print_revision_info(self):
        """
        Prints the info on the Revision phase.
        """
        print "*** RESUMEN ***"
        print "Tiempo de inicio:", colored(self.rstime, "cyan")
        print "Tiempo de finalización:", colored(self.retime, 'cyan')
        print "Duración:", colored(self.rtime, 'cyan'), "ms, =",
        print colored(self.rtime / float(1000), 'cyan'), "sec,"
        try:
            print "Porcentaje de la sesión dedicado a la fase de revisión:",
            print colored((self.rtime / float(self.ttime)) * 100, 'cyan'), "%"
        except NameError:
            self.st = max(int(self.keys[-1][6]), int(self.openClicks[-1][6]))
            self.st -= int(self.openClicks[-2][6])
            print (self.rtime / float(self.st)) * 100, "%"

    def print_total_session_info(self):
        """
        Prints the general info on the session.
        """
        print "*** SESIÓN ***"
        try:
            print "Tiempo total:", colored(self.ttime, 'cyan'), "ms =",
            print colored(self.ttime / float(1000), 'cyan'), "sec =",
            print colored(self.ttime / float(1000 * 60), 'cyan'), "min"
        except NameError:
            self.st = max(int(self.keys[-1][6]), int(self.openClicks[-1][6]))
            self.st -= int(self.openClicks[-2][6])
            print "Tiempo total:", colored(self.stime, "cyan"), "ms =",
            print colored(self.stime / float(1000), 'cyan'), "sec =",
            print colored(self.stime / float(1000 * 60), 'cyan'), "min"

    def get_orientation_info(self):
        """
        Returns a pair with the start time and end time of the orientation
        phase in milliseconds.
        """
        return (self.ostime, self.oetime)

    def get_drafting_info(self):
        """
        Returns a pair with the start time and end time of the drafting phase
        in milliseconds.
        """
        return (self.dstime, self.detime)

    def get_revision_info(self):
        """
        Returns a pair with the start time and end time of the revision phase
        in milliseconds.
        """
        return (self.rstime, self.retime)

    def get_total_session_time(self):
        """
        Returns the total time of the session.
        """
        return self.ttime
