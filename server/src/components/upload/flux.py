"""Upload and calculations with fluxes.

FluxModel handles the upload of models containing forward/reverse
or net/exchange fluxes. Flux establishes the forward and reverse
flux for each reaction.
"""

import csv
import re

from src.errors import handler
from src.validation import flux_upload

REACTION_NAME = re.compile(r'([^\s\+]\S*)\s*(?:[(\[](?:[\S]*)[)\]])?')


class FluxModel():
    """Establishes valid flux model based on header and sets fluxes.

    Attributes:
        file: UTF-8 encoded csv file.
        flux_type: Flux type as string, either FORWARD_REVERSE or NET_EXCHANGE
        fluxes: A dictonary with forward and reverse fluxes for a reaction.
    """
    def __init__(self, file):
        self._file = None
        self.file = file.read().decode('utf-8')

        self._flux_type = None
        self.flux_type = self.file['header']

        self._fluxes = None
        # self.fluxes = self.file['data']

    @property
    def file(self):
        """Parses file to header and content.

        Each row is represented as a dictonary with the keys 'reaction',
        'first_flux', 'second_flux'.

        Args:
            content: Decoded csv file.

        Returns:
            dict: A dict containing the file header and a list of dictonaries
                for each row with the model data.
        """
        return self._file

    @file.setter
    def file(self, content):
        content = [{
            'reaction': row[0],
            'first_flux': row[1],
            'second_flux': row[2]
        } for row in csv.reader(content.splitlines())]

        self._file = {'header': content[0], 'data': content[1:]}

    @property
    def flux_type(self):
        """Either FORWARD_REVERSE or NET_EXCHANGE.

        Args:
            header: A dict with the key 'first_flux' for the
                first header and 'second_flux' for the second header.

        Returns:
            string: A string representing the flux type:

        Raises:
            InvalidUsage: The flux model type is incorrect.
        """
        return self._flux_type

    @flux_type.setter
    def flux_type(self, header):
        first_header, second_header = header['first_flux'].strip().upper(
        ), header['second_flux'].strip().upper()

        is_error, errors = flux_upload.validate_flux(first_header,
                                                     second_header)

        if is_error and errors is not None:
            raise handler.InvalidUsage(status_code=400, payload=errors)

        self._flux_type = '_'.join([first_header, second_header])

    @property
    def fluxes(self):
        """Forward and reverse fluxes for each reaction.

        Args:
            data: List of dictonaries with the keys 'reaction',
                'first_flux', 'second_flux'.

        Returns:
            dict: A dict mappings each reaction to the corresponding forward
                and reverse flux. For example:

                {'v1_forward': 1.0, 'v1_reverse': 0}
        """
        return self._fluxes

    # @fluxes.setter
    # def fluxes(self, data):
    #     self._fluxes = []

    #     for index, row in enumerate(data):
    #         reaction = REACTION_NAME.search(row['reaction']).group(1)
    #         flux = Flux(reaction, index)
    #         flux.set(self.flux_type, row['first_flux'], row['second_flux'])

    #         self._fluxes.append(flux)
