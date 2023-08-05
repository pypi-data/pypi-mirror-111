#!/usr/bin/env python

"""Tests for `pysesameos2` package."""

import pytest

from pysesameos2.helper import (
    CHProductModel,
    CHSesame2MechSettings,
    CHSesame2MechStatus,
    HistoryTagHelper,
)


class TestCHProductModel:
    def test_CHProductModel_raises_exception_on_invalid_model(self):
        with pytest.raises(AttributeError):
            CHProductModel.SS99

    def test_CHProductModel_SS2(self):
        ss2 = CHProductModel.SS2
        assert ss2.deviceModel() == "sesame_2"
        assert ss2.isLocker()
        assert ss2.productType() == 0
        assert ss2.deviceFactory().__name__ == "CHSesame2"

    def test_CHProductModel_WM2(self):
        wm2 = CHProductModel.WM2
        assert wm2.deviceModel() == "wm_2"
        assert not wm2.isLocker()
        assert wm2.productType() == 1
        assert wm2.deviceFactory() is None

    def test_CHProductModel_getByModel_raises_exception_on_invalid_arguments(self):
        with pytest.raises(ValueError):
            CHProductModel.getByModel(123)

    def test_CHProductModel_getByModel_returns_None_for_unknown_model(self):
        assert CHProductModel.getByModel("sesame_99") is None

    def test_CHProductModel_getByModel_returns_SS2(self):
        assert CHProductModel.getByModel("sesame_2") is CHProductModel.SS2

    def test_CHProductModel_getByValue_raises_exception_on_invalid_arguments(self):
        with pytest.raises(ValueError):
            CHProductModel.getByValue("0")

    def test_CHProductModel_getByValue_returns_None_for_unknown_model(self):
        assert CHProductModel.getByValue(999) is None

    def test_CHProductModel_getByValue_returns_SS2(self):
        assert CHProductModel.getByValue(0) is CHProductModel.SS2


class TestCHSesame2MechStatus:
    def test_CHSesame2MechStatus_raises_exception_on_emtry_arguments(self):
        with pytest.raises(TypeError):
            CHSesame2MechStatus()

    def test_CHSesame2MechStatus_raises_exception_on_non_string_argument(self):
        with pytest.raises(TypeError):
            CHSesame2MechStatus(10)

    def test_CHSesame2MechStatus_rawdata_locked(self):
        status = CHSesame2MechStatus(rawdata="60030080f3ff0002")

        assert status.getBatteryPrecentage() == 100.0
        assert status.getBatteryVoltage() == 6.0809384164222875
        assert status.getPosition() == -13
        assert status.getRetCode() == 0
        assert status.getTarget() == -32768
        assert status.isInLockRange()
        assert not status.isInUnlockRange()
        assert (
            str(status)
            == "CHSesame2MechStatus(Battery=100% (6.08V), isInLockRange=True, isInUnlockRange=False, Position=-13)"
        )

    def test_CHSesame2MechStatus_rawdata_unlocked(self):
        status = CHSesame2MechStatus(rawdata="5c030503e3020004")

        assert status.getBatteryPrecentage() == 100.0
        assert status.getBatteryVoltage() == 6.052785923753666
        assert status.getPosition() == 739
        assert status.getRetCode() == 0
        assert status.getTarget() == 773
        assert not status.isInLockRange()
        assert status.isInUnlockRange()
        assert (
            str(status)
            == "CHSesame2MechStatus(Battery=100% (6.05V), isInLockRange=False, isInUnlockRange=True, Position=739)"
        )

    def test_CHSesame2MechStatus_rawdata_lowpower(self):
        status = CHSesame2MechStatus(rawdata="48030080f3ff0002")
        assert status.getBatteryPrecentage() == 78
        assert status.getBatteryVoltage() == 5.912023460410557

        status2 = CHSesame2MechStatus(rawdata="48020080f3ff0002")
        assert status2.getBatteryPrecentage() == 0


class TestCHSesame2MechSettings:
    def test_CHSesame2MechSettings_raises_exception_on_emtry_arguments(self):
        with pytest.raises(TypeError):
            CHSesame2MechSettings()

    def test_CHSesame2MechSettings_raises_exception_on_non_string_argument(self):
        with pytest.raises(TypeError):
            CHSesame2MechSettings(10)

    def test_CHSesame2MechSettings(self):
        setting = CHSesame2MechSettings(
            rawdata=bytes.fromhex("efff1c0159ff85008600b201")
        )

        assert setting.isConfigured is True
        assert setting.getLockPosition() == -17
        assert setting.getUnlockPosition() == 284
        assert (
            str(setting)
            == "CHSesame2MechSettings(LockPosition=-17, UnlockPosition=284, isConfigured=True)"
        )


class TestHistoryTagHelper:
    def test_split_utf8(self):
        text_bytes = "適当に 分割すると最後の文字が壊れてしまう".encode("utf-8")

        assert text_bytes[:25].decode("utf-8") == "適当に 分割すると"

        with pytest.raises(UnicodeDecodeError) as excinfo:
            text_bytes[:26].decode("utf-8")
        assert "unexpected end of data" in str(excinfo.value)

        test_25 = HistoryTagHelper.split_utf8(text_bytes, 25)
        test_26 = HistoryTagHelper.split_utf8(text_bytes, 26)

        desired_split = [
            "適当に 分割すると".encode("utf-8"),
            "最後の文字が壊れ".encode("utf-8"),
            "てしまう".encode("utf-8"),
        ]

        assert list(test_25) == desired_split
        assert list(test_26) == desired_split

    def test_create_htag(self):
        assert (
            HistoryTagHelper.create_htag(history_tag="適当な日本語で OK")
            == b"\x15\xe9\x81\xa9\xe5\xbd\x93\xe3\x81\xaa\xe6\x97\xa5\xe6\x9c\xac\xe8\xaa\x9e\xe3\x81\xa7"
        )
