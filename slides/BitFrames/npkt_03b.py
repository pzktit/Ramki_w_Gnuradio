#!/usr/bin/env python3
# -*- coding: utf-8 -*-

#
# SPDX-License-Identifier: GPL-3.0
#
# GNU Radio Python Flow Graph
# Title: Protection of payload data
# Author: pzawadzki
# GNU Radio version: 3.10.9.2

from PyQt5 import Qt
from gnuradio import qtgui
import os
import sys
sys.path.append(os.environ.get('GRC_HIER_PATH', os.path.expanduser('~/.grc_gnuradio')))

from bsc_byte_channel import bsc_byte_channel  # grc-generated hier_block
from gnuradio import blocks
from gnuradio import fec
from gnuradio import gr
from gnuradio.filter import firdes
from gnuradio.fft import window
import signal
from PyQt5 import Qt
from argparse import ArgumentParser
from gnuradio.eng_arg import eng_float, intx
from gnuradio import eng_notation
from gnuradio import gr, pdu
from msg_pdu_gen import msg_pdu_gen  # grc-generated hier_block
from msg_pdu_print import msg_pdu_print  # grc-generated hier_block
from msg_pdu_print_as_error import msg_pdu_print_as_error  # grc-generated hier_block
from pld_decode import pld_decode  # grc-generated hier_block
from pld_encode import pld_encode  # grc-generated hier_block



class npkt_03b(gr.top_block, Qt.QWidget):

    def __init__(self):
        gr.top_block.__init__(self, "Protection of payload data", catch_exceptions=True)
        Qt.QWidget.__init__(self)
        self.setWindowTitle("Protection of payload data")
        qtgui.util.check_set_qss()
        try:
            self.setWindowIcon(Qt.QIcon.fromTheme('gnuradio-grc'))
        except BaseException as exc:
            print(f"Qt GUI: Could not set Icon: {str(exc)}", file=sys.stderr)
        self.top_scroll_layout = Qt.QVBoxLayout()
        self.setLayout(self.top_scroll_layout)
        self.top_scroll = Qt.QScrollArea()
        self.top_scroll.setFrameStyle(Qt.QFrame.NoFrame)
        self.top_scroll_layout.addWidget(self.top_scroll)
        self.top_scroll.setWidgetResizable(True)
        self.top_widget = Qt.QWidget()
        self.top_scroll.setWidget(self.top_widget)
        self.top_layout = Qt.QVBoxLayout(self.top_widget)
        self.top_grid_layout = Qt.QGridLayout()
        self.top_layout.addLayout(self.top_grid_layout)

        self.settings = Qt.QSettings("GNU Radio", "npkt_03b")

        try:
            geometry = self.settings.value("geometry")
            if geometry:
                self.restoreGeometry(geometry)
        except BaseException as exc:
            print(f"Qt GUI: Could not restore geometry: {str(exc)}", file=sys.stderr)

        ##################################################
        # Variables
        ##################################################
        self.rep = rep = 3
        self.len_key = len_key = "packet_len"
        self.fs = fs = 1000000/8
        self.fec_encoder_obj = fec_encoder_obj = fec.repetition_encoder_make(8000, rep)
        self.fec_decoder_obj = fec_decoder_obj = fec.repetition_decoder.make(8000,rep, 0.5)

        ##################################################
        # Blocks
        ##################################################

        self.pld_encode_0 = pld_encode(
            fec_encoder_obj=fec_encoder_obj,
        )
        self.pld_decode_0 = pld_decode(
            fec_decoder_obj=fec_decoder_obj,
            payload_key=len_key,
        )
        self.pdu_pdu_to_tagged_stream_0 = pdu.pdu_to_tagged_stream(gr.types.byte_t, 'packet_len')
        self.msg_pdu_print_as_error_0 = msg_pdu_print_as_error()
        self.msg_pdu_print_0 = msg_pdu_print()
        self.msg_pdu_gen_0 = msg_pdu_gen()

        self.top_layout.addWidget(self.msg_pdu_gen_0)
        self.bsc_byte_channel_0 = bsc_byte_channel(
            BER=1,
            len_key=len_key,
        )
        self.blocks_throttle2_0 = blocks.throttle( gr.sizeof_char*1, fs, True, 0 if "items" == "auto" else max( int(float(fs) * fs) if "items" == "time" else int(fs), 1) )


        ##################################################
        # Connections
        ##################################################
        self.msg_connect((self.msg_pdu_gen_0, 'pdus_out'), (self.pld_encode_0, 'pdu_in'))
        self.msg_connect((self.pld_decode_0, 'ok'), (self.msg_pdu_print_0, 'pdus_in'))
        self.msg_connect((self.pld_decode_0, 'fail'), (self.msg_pdu_print_as_error_0, 'pdus_in'))
        self.msg_connect((self.pld_encode_0, 'pdu_out'), (self.pdu_pdu_to_tagged_stream_0, 'pdus'))
        self.connect((self.bsc_byte_channel_0, 0), (self.pld_decode_0, 0))
        self.connect((self.pdu_pdu_to_tagged_stream_0, 0), (self.blocks_throttle2_0, 0))
        self.connect((self.pdu_pdu_to_tagged_stream_0, 0), (self.bsc_byte_channel_0, 0))


    def closeEvent(self, event):
        self.settings = Qt.QSettings("GNU Radio", "npkt_03b")
        self.settings.setValue("geometry", self.saveGeometry())
        self.stop()
        self.wait()

        event.accept()

    def get_rep(self):
        return self.rep

    def set_rep(self, rep):
        self.rep = rep

    def get_len_key(self):
        return self.len_key

    def set_len_key(self, len_key):
        self.len_key = len_key
        self.bsc_byte_channel_0.set_len_key(self.len_key)
        self.pld_decode_0.set_payload_key(self.len_key)

    def get_fs(self):
        return self.fs

    def set_fs(self, fs):
        self.fs = fs
        self.blocks_throttle2_0.set_sample_rate(self.fs)

    def get_fec_encoder_obj(self):
        return self.fec_encoder_obj

    def set_fec_encoder_obj(self, fec_encoder_obj):
        self.fec_encoder_obj = fec_encoder_obj
        self.pld_encode_0.set_fec_encoder_obj(self.fec_encoder_obj)

    def get_fec_decoder_obj(self):
        return self.fec_decoder_obj

    def set_fec_decoder_obj(self, fec_decoder_obj):
        self.fec_decoder_obj = fec_decoder_obj
        self.pld_decode_0.set_fec_decoder_obj(self.fec_decoder_obj)




def main(top_block_cls=npkt_03b, options=None):

    qapp = Qt.QApplication(sys.argv)

    tb = top_block_cls()

    tb.start()

    tb.show()

    def sig_handler(sig=None, frame=None):
        tb.stop()
        tb.wait()

        Qt.QApplication.quit()

    signal.signal(signal.SIGINT, sig_handler)
    signal.signal(signal.SIGTERM, sig_handler)

    timer = Qt.QTimer()
    timer.start(500)
    timer.timeout.connect(lambda: None)

    qapp.exec_()

if __name__ == '__main__':
    main()
