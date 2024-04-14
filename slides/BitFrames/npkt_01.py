#!/usr/bin/env python3
# -*- coding: utf-8 -*-

#
# SPDX-License-Identifier: GPL-3.0
#
# GNU Radio Python Flow Graph
# Title: Send message via BSC channel
# Author: pzawadzki
# GNU Radio version: 3.10.9.2

from PyQt5 import Qt
from gnuradio import qtgui
import os
import sys
sys.path.append(os.environ.get('GRC_HIER_PATH', os.path.expanduser('~/.grc_gnuradio')))

from bsc_channel import bsc_channel  # grc-generated hier_block
from gnuradio import blocks
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



class npkt_01(gr.top_block, Qt.QWidget):

    def __init__(self):
        gr.top_block.__init__(self, "Send message via BSC channel", catch_exceptions=True)
        Qt.QWidget.__init__(self)
        self.setWindowTitle("Send message via BSC channel")
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

        self.settings = Qt.QSettings("GNU Radio", "npkt_01")

        try:
            geometry = self.settings.value("geometry")
            if geometry:
                self.restoreGeometry(geometry)
        except BaseException as exc:
            print(f"Qt GUI: Could not restore geometry: {str(exc)}", file=sys.stderr)

        ##################################################
        # Variables
        ##################################################
        self.len_key = len_key = "packet_len"
        self.fs = fs = 1000000//8
        self.BER = BER = 1

        ##################################################
        # Blocks
        ##################################################

        self.pdu_tagged_stream_to_pdu_0 = pdu.tagged_stream_to_pdu(gr.types.byte_t, 'packet_len')
        self.pdu_pdu_to_tagged_stream_0 = pdu.pdu_to_tagged_stream(gr.types.byte_t, 'packet_len')
        self.msg_pdu_print_0 = msg_pdu_print()
        self.msg_pdu_gen_0 = msg_pdu_gen()

        self.top_layout.addWidget(self.msg_pdu_gen_0)
        self.bsc_channel_0 = bsc_channel(
            BER=BER,
        )
        self.blocks_throttle2_0 = blocks.throttle( gr.sizeof_char*1, fs, True, 0 if "items" == "auto" else max( int(float(fs) * fs) if "items" == "time" else int(fs), 1) )
        self.blocks_repack_bits_bb_0_0 = blocks.repack_bits_bb(1, 8, len_key, False, gr.GR_MSB_FIRST)
        self.blocks_repack_bits_bb_0 = blocks.repack_bits_bb(8, 1, len_key, False, gr.GR_MSB_FIRST)


        ##################################################
        # Connections
        ##################################################
        self.msg_connect((self.msg_pdu_gen_0, 'pdus_out'), (self.pdu_pdu_to_tagged_stream_0, 'pdus'))
        self.msg_connect((self.pdu_tagged_stream_to_pdu_0, 'pdus'), (self.msg_pdu_print_0, 'pdus_in'))
        self.connect((self.blocks_repack_bits_bb_0, 0), (self.bsc_channel_0, 0))
        self.connect((self.blocks_repack_bits_bb_0_0, 0), (self.pdu_tagged_stream_to_pdu_0, 0))
        self.connect((self.bsc_channel_0, 0), (self.blocks_repack_bits_bb_0_0, 0))
        self.connect((self.pdu_pdu_to_tagged_stream_0, 0), (self.blocks_repack_bits_bb_0, 0))
        self.connect((self.pdu_pdu_to_tagged_stream_0, 0), (self.blocks_throttle2_0, 0))


    def closeEvent(self, event):
        self.settings = Qt.QSettings("GNU Radio", "npkt_01")
        self.settings.setValue("geometry", self.saveGeometry())
        self.stop()
        self.wait()

        event.accept()

    def get_len_key(self):
        return self.len_key

    def set_len_key(self, len_key):
        self.len_key = len_key

    def get_fs(self):
        return self.fs

    def set_fs(self, fs):
        self.fs = fs
        self.blocks_throttle2_0.set_sample_rate(self.fs)

    def get_BER(self):
        return self.BER

    def set_BER(self, BER):
        self.BER = BER
        self.bsc_channel_0.set_BER(self.BER)




def main(top_block_cls=npkt_01, options=None):

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
