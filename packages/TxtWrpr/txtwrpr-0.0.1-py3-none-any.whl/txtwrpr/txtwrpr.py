
'''A wrapper for fixed column text files

This module copies a fixed column TXT file into a structure to manipulate,
and enrich.  It can also be exported into a TXT file with a different
structure than the original file.
'''

import logging
from pathlib import Path
import sys
import tempfile
import beetools
import displayfx

_VERSION = "0.0.1"
_path = Path(__file__)
_name = _path.stem

class TxtWrpr:
    '''A wrapper for fixed column text files

    This module copies a fixed column TXT file into a structure to manipulate,
    and enrich.  It can also be exported into a TXT file with a different
    structure than the original file.
    '''
    def __init__( self, p_parent_logger_name,
                  p_key_idx,
                  p_src_field_def,
                  p_src = None,
                  p_has_header = True,
                  p_verbose = False
    ):
        '''Initialize the class


        Parameters
        ----------

        Returns
        -------

        Examples
        --------
        # No proper doctest (<<<) because it is os dependent

        '''
        self.logger_name = '{}.{}'.format( p_parent_logger_name, _name )
        self.logger = logging.getLogger( self.logger_name )
        self.logger.info( 'Start' )
        self.success = False
        self.exp_data = None
        self.exp_field_def = None
        self.exp_header = None
        self.exp_pth = None
        self.has_header = p_has_header
        self.key_idx = p_key_idx
        self.member_cntr = 0
        self.parsed_data = {}
        self.src_data = None
        self.src_data = None
        self.src_field_def = p_src_field_def
        self.src_pth = None
        self.verbose = p_verbose
        self.read_txt(p_src)


    def assign_src(self, p_src):
        '''Analise the data source and assign corretly'''
        self.success = True
        if isinstance(p_src, list):
            self.src_data = p_src
            self.src_pth = list
        elif p_src:
            if isinstance(p_src, Path):
                self.src_pth = p_src
                with open( self.src_pth,'r', encoding = 'cp1252' ) as src_file:
                    self.src_data = src_file.readlines()
            else:
                msg = beetools.msg_error('{} does not exist.\nSystem terminated.'.format(self.src_pth))
                print(msg)
                self.success = False
                sys.exit()
        return self.src_data


    def read_txt( self, p_src = None, p_verbose = False ):
        '''Import fixed width column text file into a list

        Parameters
        ----------

        Returns
        -------

        Examples
        --------
        # No proper doctest (<<<) because it is os dependent

        '''
        self.assign_src(p_src)
        if self.src_data:
            if self.has_header:
                t_src_data = self.src_data[1:]
            else:
                t_src_data = self.src_data
            recs_in_file = len( self.src_data ) - 1
            if isinstance(self.src_pth, Path):
                msg = beetools.msg_display( 'Process {} ({})'.format( self.src_pth, recs_in_file ))
            else:
                msg = beetools.msg_display( 'Process data ({})'.format(recs_in_file ))
            fx_bar = displayfx.DisplayFx( _name, recs_in_file, p_msg = msg)
            for fx_cntr, rec in enumerate(t_src_data):
                key_id = str(rec[self.src_field_def[self.key_idx][ 1 ] : self.src_field_def[self.key_idx][ 2 ]].strip())
                self.parsed_data[key_id] = {}
                for field_name, field_start, field_end in self.src_field_def:
                    self.parsed_data[key_id][field_name] = rec[ field_start : field_end ].strip()
                self.member_cntr += 1
                if p_verbose:
                    fx_bar.update( fx_cntr )
            if len( self.parsed_data ) >= 0:
                self.success = True
            else:
                self.success = False
        return self.parsed_data

    def write_txt(self, p_exp_pth, p_exp_field_def, p_exp_header = True, p_verbose = False):
        '''Export fixed width column text file

        Parameters
        ----------

        Returns
        -------

        Examples
        --------
        # No proper doctest (<<<) because it is os dependent

        '''
        self.exp_pth = p_exp_pth
        self.exp_field_def = p_exp_field_def
        self.exp_header = p_exp_header
        self.exp_data = ''
        if p_exp_header:
            for field in p_exp_field_def:
                field_len = field[2] - field[1]
                self.exp_data += '{: <{field_len}}'.format(field[0][:field_len], field_len = field_len)
        self.exp_data += '\n'
        msg = beetools.msg_display( 'Process {} ({})'.format( self.exp_pth, self.member_cntr))
        fx_bar = displayfx.DisplayFx( _name, self.member_cntr, p_msg = msg)
        for fx_cntr, rec in enumerate(self.parsed_data):
            exp_rec = ''
            for field in p_exp_field_def:
                field_len = field[2] - field[1]
                if field[0] in self.parsed_data[rec]:
                    field_contents = self.parsed_data[rec][field[0]]
                else:
                    field_contents = field[3]
                exp_rec += '{: <{field_len}}'.format(field_contents, field_len = field_len)
            self.exp_data += '{}\n'.format(exp_rec)
            if p_verbose:
                fx_bar.update( fx_cntr )

        self.exp_pth.write_text(self.exp_data)
        return self.exp_data



def do_example( p_app_path = '', p_cls = True ):
    '''Eample on the usage of the class.
    '''

    def basic_example():
        '''Basic and mandatory scenario tests for certification of the class

        '''
        success = True
        dst_field_def = [
            ['OrgMemberId', 0 , 15],
            ['SurnameName', 15, 50],
            ['Gender'     , 53, 54],
            ['BirthYear'  , 59, 63]
        ]
        src_data = [
            '''OrgMemberId    SurnameName                        FedgStd  Birt''',
            '''11000120       Makoto,Rodwell                     ZIMM2378 1987''',
            '''14300133       Klaasen,Calvin Jong                RSAM2226 1987''',
            '''14300427       Van der Nat,Nicholas               RSAM2362 1979''',
            '''14300702       Mabusela,Johannes Manyedi          RSAM2250 1984''',
            '''14300753       Masango,Spencer                    ZIMM2232 1982''',
            '''14304600       Barrish,Daniel                     RSAM2252 2000''',
            '''14700077       Amonatov,Farrukh                   TJKM2632 1978''',
            '''5001668        Sriram,Jha                         INDM2396 1976''',
            '''5021103        Grover,Sahaj                       INDM2473 1995''',
            '''8700249        Jere,Daniel                        ZAMM2384 1986''',
        ]
        src_field_def = [
            ['OrgMemberId', 0 , 15],
            ['SurnameName', 15, 50],
            ['Fed'        , 50, 53],
            ['Gender'     , 53, 54],
            ['Std'        , 54, 59],
            ['BirthYear'  , 59, 63]
        ]
        key_idx = 0
        txt_file = TxtWrpr(
            _name,
            key_idx,
            src_field_def,
            p_has_header = False,
            p_verbose = True )
        success = txt_file.read_txt(src_data)
        dst_fldr = Path(tempfile.TemporaryDirectory().name)
        success = txt_file.write_txt(dst_fldr, dst_field_def)
        return success

    success = True
    b_tls = beetools.Archiver( _name,
                               _VERSION,
                               __doc__[0],
                               p_app_path = p_app_path,
                               p_cls = p_cls )
    logger = logging.getLogger( _name )
    logger.setLevel( beetools.DEF_LOG_LEV )
    file_handle = logging.FileHandler( beetools.LOG_FILE_NAME, mode = 'w' )
    file_handle.setLevel( beetools.DEF_LOG_LEV_FILE )
    console_handle = logging.StreamHandler()
    console_handle.setLevel( beetools.DEF_LOG_LEV_CON )
    file_format = logging.Formatter( beetools.LOG_FILE_FORMAT, datefmt = beetools.LOG_DATE_FORMAT )
    console_format = logging.Formatter( beetools.LOG_CONSOLE_FORMAT )
    file_handle.setFormatter( file_format )
    console_handle.setFormatter( console_format )
    logger.addHandler( file_handle )
    logger.addHandler( console_handle )

    b_tls.print_header( p_cls = p_cls )
    success = basic_example()
    beetools.result_rep( success, 'Done' )
    b_tls.print_footer()
    if success:
        return b_tls.archive_path
    return False
# end do_tests

if __name__ == '__main__':
    do_example(p_app_path=_path)
# end __main__
